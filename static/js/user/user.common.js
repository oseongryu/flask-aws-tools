var user_common = user_common || (function(){
    var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    console.dir(this.document.currentScript.src);
    return{
        init: function(e){
            console.dir(this.document.currentScript.src);
        },
        exec: function(name) {
            console.dir('exec')
            if(name == null || name == ''){
                name = 'systemInfo'
            }
            $.ajax({
                url : name,
                method : "GET",
                success : function(response) {
                    console.dir(response);
                },
                error : function(error) {
                    alert('error');
                },
            });
        },
        loadClassPath: async function(fileDir){
            var result = {}
            $.ajax({
                url : `/load-class-path`,
                method : "POST",
                async: false,
                contentType : "application/json; charset=UTF-8",
                dataType : "json",
                data : JSON.stringify({
                    "fileDir" : fileDir
                }),
                complete : function(response) {
                    if(!user_function.isEmpty(response) && response.status == 200) {
                        const responsePath = response.responseText;
                        $.ajax({
                            url : `${responsePath}`,
                            method : "GET",
                            async: false,
                            complete : function(response) {
                                if(!user_function.isEmpty(response) && response.status == 200) {
                                    result = response.responseText;
                                }
                            },
                            exception : function(error) {
                                user_modal.error();
                                result = {}
                            },
                        });
                        return result;
                    }
                },
                exception : function(error) {
                    user_modal.error();
                    result = {}
                },
            });
            return result;
        },
        loadType: async function(fileName){
            console.dir(`/load-type ${fileName}`);
            var result = {};
            if (fileName.includes('setting-file-dir')) {
                result = await user_common.loadTypePost(fileName)
            } else if (fileName.split("/").length > 1) {
                result = await user_common.loadTypePost(fileName)
            } else {
                result = await user_common.loadTypeGet(fileName)
            }
            return result;
        },
        loadTypeGet: async function(fileName){
            var result = {}
            $.ajax({
                url : `/load-type/json/${fileName}`,
                method : "GET",
                async: false,
                headers: {
                    'x-access-tokens': sessionStorage.getItem('token')
                },
                data : {
                },
                complete : function(response) {
                    // user_modal.success();
                    if(!user_function.isEmpty(response) && response.status == 200) {
                        result = response.responseText;
                    }
                },
                exception : function(error) {
                    user_modal.error();
                    result = {}
                },
            });
            return result;
        },
        loadTypePost: async function(fileName) {
            var result = {}
            $.ajax({
                url : `/load-type`,
                method : "POST",
                async: false,
                contentType : "application/json; charset=UTF-8",
                dataType : "json",
                headers: {
                    'x-access-tokens': sessionStorage.getItem('token')
                },
                data : JSON.stringify({
                    "fileId" : fileName,
                    "type": "project"
                }),
                complete : function(response) {
                    // user_modal.success();
                    if(!user_function.isEmpty(response) && response.status == 200) {
                        result = response.responseText;
                    }
                },
                exception : function(error) {
                    console.log(error)
                    user_modal.error();
                    result = {}
                },
            });
            return result;
        },
        run_command: async function(){
            const command = $("#command").val();
            $.ajax({
                url: "/run-command",
                type: "POST",
                contentType: "application/json",
                headers: {
                    'x-access-tokens': sessionStorage.getItem('token')
                },
                data: JSON.stringify({ command: command }),
                complete : function(response) {
                    // user_modal.success();
                    const result = response.responseJSON;
                    if(!user_function.isEmpty(response) && response.status == 200) {
                        $("#output").text(result.output || result.error);
                    }
                },
                exception : function(error) {
                    console.log(error)
                    user_modal.error();
                    result = {}
                },
            });
        }
    }
})();

