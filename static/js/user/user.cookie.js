var user_cookie = user_cookie || (function(){
	var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    console.dir(this.document.currentScript.src);
    return{
        init: function(e){
            console.dir(this.document.currentScript.src);
        },
		getCookie: function getCookie(name) {
            let matches = document.cookie.match(new RegExp(
                "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
            ));
            return matches ? decodeURIComponent(matches[1]) : undefined;
        },
        setCookie: function setCookie(name, value, options = {}) {
            // user_cookie.setCookie('listOSText', _listOSText, {secure: false, 'max-age': 86400e3});
            options = {
                path: '/',
                ...options
            };

            if (options.expires instanceof Date) {
                options.expires = options.expires.toUTCString();
            }

            let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

            for (let optionKey in options) {
                updatedCookie += "; " + optionKey;
                let optionValue = options[optionKey];
                if (optionValue !== true) {
                    updatedCookie += "=" + optionValue;
                }
            }

            document.cookie = updatedCookie;
        }
	}
})();

