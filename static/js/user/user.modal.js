var user_modal = user_modal || (function(){
    var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    console.dir(this.document.currentScript.src);
    return{
        settingData: [],
        init: function(e){
            console.dir(this.document.currentScript.src);
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
        initSettingPopup: async function (fileDir) {
            var result = await user_common.loadClassPath(fileDir);
            if(user_modal.settingData !=  null) {
                user_modal.settingData = JSON.parse(result)
                user_session.load();
                user_modal.settingPopup(user_modal.settingData);
            }
        },
        val: function(id) {
            var data = user_json.getVal(user_modal.settingData, id);
            return data;
        },
        settingPopup : function(paramData){
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
                    $("[name='"+key+"']").val(sessionStorage.getItem(key));
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
    }
})();

