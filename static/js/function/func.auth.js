var func_auth = func_auth || (function(){
  var console = window.console || {log:function(){},error:function(){},warn:function(){},dir:function(){}};
  console.dir(this.document.currentScript.src);
  return{
      init: function(e){
          console.dir(this.document.currentScript.src);
      },
      auth: async function(userId, userPw) {
        var authHeader = 'Basic ' + btoa(userId + ':' + userPw);
        $.ajax({
            url: '/api/auth',
            method: 'POST',
            contentType: 'application/json',
            headers: {
              'Authorization': authHeader
            },
            data: JSON.stringify({ username: userId, password: userPw }),
            success: function (response) {
              user_session.set('token', response.token);
              window.location.href = '/';
            },
            error: function(error) {
              console.error('Error:', error);
              alert('Login failed');
            }
        });
    },
  }
})();

