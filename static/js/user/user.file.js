var user_file = user_file || (function () {
    var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    console.dir(this.document.currentScript.src);
    return {
        init: function (e) {
            console.dir(this.document.currentScript.src);
        },
        fileList: async function (fileDir, type) {
            console.dir('fileList');
            var result = {}
            $.ajax({
                url: `/file/file-list`,
                method: "POST",
                async: true,
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

