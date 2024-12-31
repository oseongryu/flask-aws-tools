var user_common = user_common || (function(){
    var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    console.dir(this.document.currentScript.src);
    return{
        init: function(e){
            console.dir(this.document.currentScript.src);
        },
        loadClassPath: async function(fileDir){
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
        loadTypePost: async function(fileName) {
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
        fileList: async function (fileDir, type) {
            console.dir('fileList');
            var result = {}
            $.ajax({
                url: `/file/file-list`,
                method: "POST",
                async: false,
                headers: {
                    'x-access-tokens': user_session.get('token')
                },
                data: {
                    fileDownloadDir: fileDir,
                    type: type
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
        pythonExec: function (rowNum, envPath, scriptPath) {
            console.dir('python-exec');
            if (confirm("실행하시겠습니까?")) {
                $.ajax({
                    url: "/api/automation/python-exec",
                    method: "POST",
                    data: {
                        id: rowNum,
                        pythonEnvPath: envPath,
                        pythonPath: scriptPath,
                    },
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
        pythonExecAll: function (rowNum) {
            console.dir('python-exec-all');
            $.ajax({
                url: "/api/automation/python-exec-all",
                method: "POST",
                data: {
                    id: rowNum
                },
                headers: {
                    'x-access-tokens': user_session.get('token')
                },
                complete: function (response) {
                    // user_modal.success();
                },
                exception: function (error) {
                    // user_modal.error();
                },
            });
        },
    }
})();

