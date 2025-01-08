var user_session = user_session || (function(){
	var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    // console.log(this.document.currentScript.src);
	return{
        init: function(e){
            console.log(this.document.currentScript.src);
        },
        load: function(event){
            for (var rowIdx = 0; rowIdx < sessionStorage.length; rowIdx++ ){
                var key = sessionStorage.key(rowIdx);
                if(!user_function.isEmpty(user_session.get(key))){
                    $('#'+ key).val(user_session.get(key));
                }
            }
        },
        get: function(key){
            return sessionStorage.getItem(key);
        },
        set: function(key, value){
            sessionStorage.setItem(key, value);
        },
        remove: function(key){
            sessionStorage.removeItem(key);
        },
	}
})();

