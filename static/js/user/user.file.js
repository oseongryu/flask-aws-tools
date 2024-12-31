var user_file = user_file || (function () {
    var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    console.dir(this.document.currentScript.src);
    return {
        init: function (e) {
            console.dir(this.document.currentScript.src);
        },
        sourceDownload: function () {
            document.addEventListener('DOMContentLoaded', () => {
                user_file.downloadTemplate('source.html', document.documentElement.outerHTML); //현재 웹페이지 전체 소스 선택
            });
        },
        //Download HTML Template Source
        downloadTemplate: function (filename, text) {
            let element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
            element.setAttribute('download', filename);
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        },
        downloadJSON: function (filename, text) {
            let element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + JSON.stringify(text, null, 4));
            element.setAttribute('download', filename);
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        },
        fileScan: async function (fileDir) {
            console.dir('fileScan')
            var result = {}
            $.ajax({
                url: "/api/file/file-scan",
                method: "GET",
                async: false,
                headers: {
                    'x-access-tokens': sessionStorage.getItem('token')
                },
                complete: function (response) {
                    // user_modal.success();
                    if (!user_function.isEmpty(response) && response.status == 200) {
                        result = response.responseText;
                    }
                },
                exception: function (error) {
                    user_modal.error();
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
                async: true,
                headers: {
                    'x-access-tokens': sessionStorage.getItem('token')
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
        localExec: function (e) {
            console.dir('localExec');
            location.href = 'sample://0'
        },
        remoteExec: function (e) {
            console.dir('remoteExec');
            $.ajax({
                url: "/api/automation/remote-exec",
                method: "POST",
                data: {
                    id: "5"
                },
                headers: {
                    'x-access-tokens': sessionStorage.getItem('token')
                },
                complete: function (result) {
                    user_modal.success();
                }
            });
        },
        pythonExec: function (rowNum, envPath, scriptPath) {
            if (confirm("실행하시겠습니까?")) {
                console.dir('python-exec');
                $.ajax({
                    url: "/api/automation/python-exec",
                    method: "POST",
                    data: {
                        id: rowNum,
                        pythonEnvPath: envPath,
                        pythonPath: scriptPath,
                    },
                    headers: {
                        'x-access-tokens': sessionStorage.getItem('token')
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
                    'x-access-tokens': sessionStorage.getItem('token')
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

