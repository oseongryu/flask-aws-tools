var service_auth = service_auth || (function(){
    var console = window.console || {log:function(){},error:function(){},warn:function(){},dir:function(){}};
    console.log(this.document.currentScript.src);
    return{
        init: function(e){
            console.log(this.document.currentScript.src);
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

