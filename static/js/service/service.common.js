var service_common = service_common || (function(){
    var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    console.log(this.document.currentScript.src);
    return{
        init: function(e){
            console.log(this.document.currentScript.src);
        },
        loadTypeGet: async function(fileId, type){
            var result = {}
            $.ajax({
                url : `/load-type/${type}/${fileId}`,
                method : "GET",
                async: false,
                headers: {
                    'x-access-tokens': user_session.get('token')
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
        loadTypePost: async function(fileId, type) {
            var result = {}
            $.ajax({
                url : `/load-type`,
                method : "POST",
                async: false,
                contentType : "application/json; charset=UTF-8",
                dataType : "json",
                headers: {
                    'x-access-tokens': user_session.get('token')
                },
                data : JSON.stringify({
                    "fileId" : fileId,
                    "type": type
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
        loadFileJson: async function(fileId, type){
            var result = {}
            $.ajax({
                url : `/load-class-path`,
                method : "POST",
                async: false,
                contentType : "application/json; charset=UTF-8",
                dataType : "json",
                headers: {
                    'x-access-tokens': user_session.get('token')
                },
                data : JSON.stringify({
                    "fileId" : fileId,
                    "type": type
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
        fileList: async function (filePath, type, sort_key, sort_order) {
            var result = {}
            $.ajax({
                url: `/api/common/select-file`,
                method: "POST",
                async: false,
                headers: {
                    'x-access-tokens': user_session.get('token')
                },
                data: {
                    filePath: filePath,
                    type: type,
                    sort_key: sort_key,
                    sort_order: sort_order
                },
                complete: function (response) {
                    // user_modal.success();
                    if (!user_function.isEmpty(response) && response.status == 200) {
                        result = response.responseText;
                    }
                },
                exception: function (error) {
                    user_modal.error();
                    result = {}
                },
            });
            return result;
        },
        pythonExec: function (type, args1) {
            if (confirm("실행하시겠습니까?")) {
                $.ajax({
                    url: `/api/common/python-exec?type=${type}&args1=${args1}`,
                    method: "GET",
                    headers: {
                        'x-access-tokens': user_session.get('token')
                    },
                    complete: function (response) {
                        // user_modal.success();
                    },
                    exception: function (error) {
                        user_modal.error();
                    },
                });
            }
        },
        pythonExecPost: function (type, args1) {
            if (confirm("실행하시겠습니까?")) {
                $.ajax({
                    url: `/api/common/python-exec`,
                    type: "POST",
                    contentType: "application/json",
                    headers: {
                        'x-access-tokens': user_session.get('token')
                    },
                    data: JSON.stringify({ "type": type, "args1": args1 }),
                    complete: function (response) {
                        // user_modal.success();
                    },
                    exception: function (error) {
                        user_modal.error();
                    },
                });
            }
        },
        runCommand: async function(){
            const command = $("#command").val();
            $.ajax({
                url: "/api/common/run-command",
                type: "POST",
                contentType: "application/json",
                headers: {
                    'x-access-tokens': user_session.get('token')
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

