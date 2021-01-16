

 $(document).ready(function(){
  if (window.localStorage){
     $('#logout').on('click', function(){
        localStorage.setItem("app-logout", 'logout' + Math.random());
        return true;
     });
  }
})


window.addEventListener('storage', function(event){
  if (event.key == "app-logout") {
    window.location = $('#logout').attr('href');
  }
}, false);
