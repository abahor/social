import random
import string

from flask import Blueprint, render_template, redirect, request, url_for, abort, \
    Response, jsonify, send_file, session, send_from_directory
from flask_login import login_required, current_user

from myproject import db
from myproject.main.forms import searchForm, updatePOSTForm
from myproject.main.handle_media import handle
from myproject.models import Posts, Users, media
from myproject.posts.forms import createPost

main = Blueprint('main', __name__, template_folder='temp')


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


@main.route('/', methods=['get', 'post'])
def index():
    medied = ''
    form = createPost()
    ed = ''
    if form.validate_on_submit():
        if current_user.is_authenticated:
            if form.media.data:
                medied = handle(form.media.data)
                try:
                    if medied:
                        ed = media(media_url=medied[0])
                        db.session.add(ed)
                        db.session.commit()
                except Exception as e:
                    db.session.rollback()
            if ed:
                # print(ed.id)
                new_post = Posts(text=form.text.data, title=form.title.data, user_id=current_user.id, images=ed.id,
                                 m=medied[1])
            else:
                new_post = Posts(form.text.data, form.title.data, current_user.id)
            try:
                # print('----------------------------------'
                #       '-----------------------------------'
                #       ''
                #       ''
                #       '-----------------------------------')
                db.session.add(new_post)
                db.session.commit()

                try:
                    d = int(new_post.id) - 100000
                    re = Posts.query.get(d)
                    if re:
                        db.session.delete(re)
                        db.session.commit()
                except:
                    db.session.rollback()
                return redirect(url_for('main.index'))
            except Exception as e:
                db.session.rollback()
                # return 'something wrong'
                return str(e)
        else:
            return redirect(url_for('main.index'))

    return render_template('main.html', new_post=form)


@main.route('/search')
@login_required
def search():
    search = request.args.get('q')
    # print(search)
    if not search:
        abort(404)
    posts = Posts.query.search(search).all()
    return render_template('search.html', posts=posts)


# @main.route('/index')
# @login_required
# def create():
# form = createPost()
# if form.validate_on_submit():
#     new_post = Posts(form.text.data, form.media.data, current_user.id)
#     try:
#         db.session.add(new_post)
#         db.session.commit()
#         return redirect(url_for('main.index'))
#     except:
#         db.session.rollback()
#         return 'something wrong'

@main.route('/load')
def load():
    d = Posts.query.order_by(Posts.date.desc()).all()
    # print(d)
    posts = len(d)
    # print(len(d))
    quantity = 3
    # print(d)
    try:
        counter = int(request.args.get('c'))
    except:
        return 'go to hell'

    # if counter == 0:
    #     # print(f'returing  Posts from 0 to {quantity}')
    #     # print(d[0: quantity])
    #     post_schema = Postsshema(many=True)
    #     # print(post_schema)
    #     k = post_schema.dump(d[0: quantity]).data
    #     arr = []
    #     # for value in d[0:quantity]:
    #     #     print(value)
    #     #     temp = render_template('load.html', post=value)
    #     #     arr.append(temp)
    #     td = d[0:quantity]
    #     temp = make_response(render_template('load.html', posts=td))
    #     return str(temp)
    # time.sleep(5)
    if counter == posts or counter > posts:
        # print("No more posts")
        return ''
    else:
        # print(f'Returning Posts {counter} to {counter + quantity}')
        # print(f'returing  Posts from 0 to {quantity}')
        # print(d[counter:counter + quantity])
        # post_schema = Postsshema(many=True)
        # print(post_schema)
        # k = post_schema.dump(d[counter: counter + quantity]).data
        # print(k)
        # arr = []
        # for value in k:
        #     temp = make_response(render_template('load.html'), post=value)
        #     arr.append(temp)
        g = []
        td = d[counter: counter + quantity]
        for i in td:
            if i.media.media_url:
                session['this_is_for'] = randomString()
                temp = render_template('load.html', post=i)
                # print(temp)
                tt = {'rep': temp, 'scr': '/controllers?c=' + session['this_is_for']}
            else:
                session['this_is_for'] = None
                temp = render_template('load.html', post=i)
                tt = {'rep': temp}
            g.append(tt)
        session['this_is_for'] = None
        # r = json.dumps(g)
        # temp = make_response(render_template('load.html', posts=td))
        # for i in td:
        #     g.append(i.id)
        # g = tuple(g)
        # print(g)
        return jsonify(g)


@main.route('/post')
def post_loader():
    try:
        i = int(request.args.get('c'))
        post = Posts.query.get_or_404(i)
    except:
        return abort(404)
    return render_template('loader.html', post=post)


@main.route("/posts")
def postsd():
    # try:
    fom = searchForm()
    # print(request.args.get('ipo'))
    try:
        d = int(request.args.get('ipo'))
    except:
        abort(404)
    post = Posts.query.get(d)
    if not post:
        abort(404)
    # exte = post.m
    # med = False
    # if exte == 'b':
    #     med = 'img'
    # elif exte == 'v':
    #     med = 'video'

    return render_template('post.html', post=post, fom=fom)
    # except Exception as e:
    #         print(e)
    #         abort(403)


# ------------------------------        NEED TO BE FIXED
@main.route('/post/<int:post_id>/update')
@login_required
def update(post_id):
    posted = Posts.query.get_or_404(post_id)
    if posted.author != current_user:
        abort(404)
    form = updatePOSTForm()
    if form.validate_on_submit():
        posted.title = form.title.data
        posted.text = form.text.data
        if form.media.data:
            posted.media.media_url = handle(form.media.data)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return abort(404)
    form.title.data = posted.title
    form.text.data = posted.text

    return render_template('update_post.html', form=form,media=posted.media.id,post=posted)


# ----------------------------------------------------------------------


@main.route('/post/<int:post_id>/delete', methods=['post'])
@login_required
def delete(post_id):
    posted = Posts.query.get_or_404(post_id)
    # print(posted.author)
    if posted.author.id != current_user.id:
        abort(404)
    try:
        db.session.delete(posted)
        db.session.commit()
    except:
        db.session.rollback()
    return redirect(url_for('main.index'))


@main.route('/user', methods=['get'])
def user():
    try:
        use = int(request.args.get('re'))
        print(use)
        # print(user)
        re = Users.query.get_or_404(use)
        print(re)
        # print(re)
        # di = {'profile': re.profile_pic}
        # print(re.profile_pic)
        return render_template("user.html",user=re)
    except:
        return ''


# def clever_function(de):
#     exte_image = ['jpg', 'png']
#     exte_video = ['mp4', 'mkv']
#     tag = de.split('.')[-1]
#     if tag in exte_image:
#         sad = f'<img src="{de}" class="media">'
#         sad = bytes(sad, 'utf-8')
#         return sad
#     elif tag in exte_video:
#         sad = f'<video src="{de}" class="media"></video>'
#         sad = bytes(sad, 'utf-8')
#         return sad

@main.route('/<int:name>')
def name(name):
    # b = current_app.root_path
    # print('-------------------------------')
    get = media.query.get(name)
    # # print(get)
    # # print(get.media_url)
    # v = open(b + 'static/media/' + get.media_url,'rb')
    # d = v.read()
    # v.close()
    return send_file('protected/' + get.media_url)
    # return d


@main.route('/controllers')
def controllers():
    re = request.args.get('c')
    if not re:
        return ''

    return render_template('dd.js', d=re)


# def generate_stock_table():
#     yield render_template('stock_header.html')
#     for stock in Posts.query.all():
#         yield render_template('stock_row.html', stock=stock)
#     yield render_template('stock_footer.html')

# @main.route('/static')
# def deny_the_access():
#     abort(404)
#     return ''

# @main.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path,'static'),'icons8-social-octopus-48.png', mimetype='image/vnd.microsoft.icon')


# @main.route('/stock-table')
# def stock_table():
#     return Response(generate_stock_table())



@main.route('/favicon.ico')
def favicon():
    return send_from_directory("static",filename='icons8-social-octopus-48.png'
                               , mimetype='image/vnd.microsoft.icon')


@main.route('/about_me')
def about_me():
    return render_template('about_me.html')


#@main.route('/rochester')
#def rochester():
#    return render_template('rochester.html')


#@main.route('/about_admission')
# def about_admission():
#    return render_template('about_admission.html')


@main.route('/privacypolicy')
def privacy():
    return render_template('privacypolicy.html')

#@main.route('/stanford')
#def stanford():
#    return render_template('stanford.html')


#@main.route('/fateh.zip')
#def fateh():
#        return send_from_directory("static",filename='dad.rar'
#                               )
