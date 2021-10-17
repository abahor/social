var scroller = document.querySelector('#scroller');
var template = document.querySelector('#post_template');
var loaded = document.querySelector('#loaded');
var sentinel = document.querySelector('#sentinel');
var counter = 0;

function loadItem() {

//  fetch('/load?c='+counter).then((response) => {
//    data = response
//      if (!data.length){
//        sentinel.innerHTML = 'No more posts';
//      }
//
//     console.log(data)
//      // for (var i = 0; i < data.length; i++){
//        let template_cloe = document.importNode(template.content,true)
//        let template_clone = template.content.cloneNode(true);
//        template_clone.innerHTML = data
//         template_clone.querySelector('#title').innerHTML = data[i].title;
//         var x = new XMLHttpRequest();
//         x.onreadystatechange = function() {
//             if (this.readyState == 4 && this.status == 200) {
// //                alert(this.responseText)
//                 console.log(typeof(template.content.cloneNode(true)));
//                 template_clone.querySelector('#link').src  = this.responseText;
//             }
//         }
//         x.open('GET','/user?c='+ data[i].author, async=false)
//         x.send()
//         template_clone.querySelector('#date').innerHTML = strftime('%Y-%m-%d',data[i].date);
//         template_clone.querySelector('#content').innerHTML = data[i].text;
//         template_clone.querySelector('#linktopost').href = '/posts?ipo='+data[i].id
//         console.log(data[i].images)
// if (data[i].media){
//   d = data[i].m
//   if (d == 'b') {
//     template_clone.querySelector('#mediaimg').src = data[i].media
//   } else if (d == 'v') {
//     template_clone.querySelector('#mediavideo').src = data[i].media;
//     template_clone.querySelector('#mediavideo').style.display = 'block';
//   }
// }
// console.log(data[i].images);
        var d = new XMLHttpRequest();
                 d.onreadystatechange = function() {
             if (this.readyState == 4 && this.status == 200) {
                 if (!this.responseText){
                    sentinel.innerHTML = 'No more posts';
                    return;
                 }
//                 var r = JSON.parse(this.responseText)
//                 var re = document.createElement('div')
//                 re.innerHTML = r.rep
//                 var scr = document.createElement('script')
//                 scr.src = r.scr
                    var ter = JSON.parse(this.responseText)
                    var i;
                    for (i of ter){

                    var rererer = document.createElement('div');
                    rererer.innerHTML= i.rep
                    scroller.appendChild(rererer);
                    if(i.scr){
                       var rdd =document.createElement('script')
                       rdd.src = i.scr
                       scroller.appendChild(rdd)
                    }

                    }
//                 template_clone.innerHTML  = this.responseText;
//                 document.getElementsByTagName('template')[counter].innerHTML  = this.responseText;
//                 console.log(template_clone.innerHTML)
//                 console.log(template_clone)
                 counter += 3;
////                 scroller.appendChild(template_clone);
//                   scroller.appendChild(re)
             }
         }
//        scroller.appendChild(template_clone);
        d.open('GET','/load?c='+ counter, async=false)
        d.send()

//        loaded.innerHTML = counter + ' items loaded';
      // }
    }

var intersectionObserver = new IntersectionObserver(entries => {
  if (entries[0].intersectionRatio <= 0){
    return;
  }
  loadItem();
});
intersectionObserver.observe(sentinel);
