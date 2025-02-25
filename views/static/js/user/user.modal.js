var user_modal = user_modal || (function(){
    var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    // console.log(this.document.currentScript.src);
    return{
        settingData: [],
        init: function(e){
            console.log(this.document.currentScript.src);
        },
        message: function(text) {
            $('#modalContent').html(text);
            $('#modal').modal('show');
        },
        success: function(text){
            if(user_function.isEmpty(text)) text = 'success';
            user_modal.message(text);
        },
        error: function(text) {
            if(user_function.isEmpty(text)) text = 'error';
            user_modal.message(text);
        },
        confirm : function(text){
            $("#confirmModalContent").html(text);
            $("#confirmModal").modal('show');

            $('#confirmModalOK').click(function(event) {
                $("#confirmModal").modal('hide');
                return true;
            });
        },
        val: function(id) {
            var data = user_json.getVal(user_modal.settingData, id);
            return data;
        },
        initModal: async function (fileDir, type) {
            var result = await service_common.loadFileJson(fileDir, type);
            if(user_modal.settingData !=  null) {
                user_modal.settingData = JSON.parse(result)
                user_session.load();
                user_modal.setting(user_modal.settingData);
            }
        },
        setting : function(paramData){
            var settingData = paramData
            $('#btnSetting').click(function(event){
                var result = user_json.flatten(settingData);
                $("#settingModalContent").html("<div id='settingDiv' class='table-responsive' style='width:100%; height:60%; overflow:auto'></div>");
                $("#settingDiv").html("<table id='settingTable' class='table no-margin'></table>");
                $("#settingTable").append("<thead><tr>"
                    + "<th style='text-align:left; width:40%'>key</th>"
                    + "<th style='text-align:left; width:60%'>value</th></tr></thead>")
                $("#settingTable").append("<tbody>");
                Object.keys(result).map(key=> {
                    $("#settingTable").append("<tr>"
                        + "<td style='text-align:left'>"+ key + "</td>"
                        + "<td style='text-align:center'><input type='text' name='"+key+"' style='width: 100%; border: none;' autocomplete='off' ></td>"
                        + "</tr>");
                    $("[name='"+key+"']").val(user_session.get(key));
                })
                $("#settingTable").append("</tbody>");

                $("#settingModal").modal({show:true});
            });
            $("#modalBtnSave").click(function(event){
                var result = user_json.flatten(settingData);
                Object.keys(result).map(key=> {
                    sessionStorage.setItem(key, $("[name='"+key+"']").val())
                })
                $("#settingModal").modal('hide');
            });
        },
        initLogModal: async function () {
            console.log("logModal");
            $("#btn_log").click(function (event) {
            const logWindow = window.open("", "LogWindow", "width=600,height=400");
                logWindow.document.write("<html><head><title>Real-time Log</title></head><body><div id='log'></div></body></html>");
                const logElement = logWindow.document.getElementById("log");
                const eventSource = new EventSource("/api/common/real-log");
                eventSource.onmessage = function (event) {
                var text = event.data;
                if (text.includes("/api/")) {
                    const newElement = document.createElement("div");
                    newElement.textContent = event.data;
                    logElement.insertBefore(newElement, logElement.firstChild);
                }
                };
            });
        }
    }
})();

