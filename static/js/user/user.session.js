var user_session = user_session || (function(){
	var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    console.dir(this.document.currentScript.src);
	return{
        init: function(e){
            console.dir(this.document.currentScript.src);
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
            return user_session.get(key);
        },
        set: function(key, value){
            sessionStorage.setItem(key, value);
        },
	}
})();

