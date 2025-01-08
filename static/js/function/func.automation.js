var func_automation = func_automation || (function(){
    var console = window.console || {log:function(){},error:function(){},warn:function(){},dir:function(){}};
    console.log(this.document.currentScript.src);
    return{
        settingData: [],
        AUTOMATION_SCREENSHOT_PATH: "automation-screenshot",
        AUTOMATION_INIT_PATH: "automation-init",
        AUTOMATION_POPUP_PATH: "automation-popup",
        init: function(e){
            console.log(this.document.currentScript.src);
        },
        gridRowClick: function (fileCustomDir) {
            user_viewer.clean();
            func_automation.screenshotList(func_automation.AUTOMATION_SCREENSHOT_PATH + fileCustomDir, 'fileName');
        },
        clearGrid: function (defaultViewId, defaultTable) {
            $(defaultViewId).html(`<table id=${defaultTable} class='table no-margin'></table>`);
        },
        processList: async function(filePath, type) {
            // console.log('processList');
            var defaultName = "process";
            var defaultView = `${defaultName}View`;
            var defaultTable = `${defaultName}Table`;
            var defaultViewId = `#${defaultView}`;
            var defaultTableId = `#${defaultTable}`;

            var result = await service_common.loadTypePost(filePath, type);


            var resultList = JSON.parse(result);
            this.clearGrid(defaultViewId, defaultTable);
            $(defaultTableId).append(
                "<thead><tr>"
                + "<th style='text-align:center; font-size:10px;'>No</th>"
                + "<th style='text-align:center; font-size:10px;'>실행명</th>"
                + "<th style='text-align:center; font-size:10px;'>실행</th>"
                + "</tr></thead>");

            for (var rowIdx = 0; rowIdx < resultList.length; rowIdx++) {
                var siteExecName = resultList[rowIdx].siteExecName;
                var siteExecDesc = resultList[rowIdx].siteExecDesc;
                func_automation.settingData.push({siteExecName: siteExecName, siteExecDesc: siteExecDesc})

                $(defaultTableId).append(
                    "<tr>"
                    + `<td style='text-align:left; font-size:10px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'>${rowIdx+1}</div></td>`
                    + `<td style='text-align:left; font-size:10px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'>${siteExecDesc}</div></td>`
                    + `<td style='text-align:center; font-size:10px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'><a name=${siteExecName} onclick='service_common.pythonExec("automation", ${rowIdx});'>실행</a></div></td>`
                    + "</tr>");
            }
        },
        processResultList:async function(filePath, type) {
            // console.log('processResultList');
            var defaultName = "processResult";
            var defaultView = `${defaultName}View`;
            var defaultTable = `${defaultName}Table`;

            var defaultViewId = `#${defaultView}`;
            var defaultTableId = `#${defaultTable}`;
            var result =await service_common.fileList(filePath, type, "depth3_dir", "desc");


            var resultList = JSON.parse(result);
            this.clearGrid(defaultViewId, defaultTable);
            $(defaultTableId).append(
                "<thead><tr>"
                + "<th style='text-align:center; font-size:10px;'>No</th>"
                + "<th style='text-align:center; font-size:10px;'>실행결과</th>"
                + "<th style='text-align:center; font-size:10px;'>시간</th>"
                + "<th style='text-align:center; font-size:10px; display: none;'>param</th>"
                + "</tr></thead>");

            // 내림차순정렬
            // var sortList = user_function.sortDesc(resultList, 'depth3Dir');
            for (var rowIdx = 0; rowIdx < resultList.length; rowIdx++) {
                var depth2Dir = resultList[rowIdx].depth2Dir;
                var depth3Dir = resultList[rowIdx].depth3Dir;
                var varDir = "/" + depth2Dir + "/" + depth3Dir;
                var displayDir = depth2Dir + "/" + depth3Dir;
                var varTime = depth3Dir.split('_')[1];
                var displayTime = varTime.substring(0, 2) + ":" + varTime.substring(2, 4) + ":" + varTime.substring(4, 6)
                func_automation.settingData.map(row => {
                    if (row.siteExecName == depth2Dir) displayDir = row.siteExecDesc
                });

                $(defaultTableId).append(
                    "<tr>"
                    + `<td style='text-align:left; font-size:10px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'>${rowIdx + 1}</div></td>`
                    + `<td style='text-align:left; font-size:10px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'>${displayDir}</div></td>`
                    + `<td style='text-align:left; font-size:10px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'>${displayTime}</div></td>`
                    + `<td style='text-align:left; font-size:10px; display: none;'><div>${varDir}</div></td>`
                    + "</tr>"
                );
            }

            $(defaultTableId + " tr").click(function () {
                // 첫번째줄선택 disabled
                if ($(this).find('th:first').html() === 'No') return;

                $(this).removeClass('before_searched');
                $(this).addClass('selected').siblings().removeClass('selected');

                var paramData = $(this).find('td:last').find('div').html();
                func_automation.gridRowClick(paramData)
            });
            $($(defaultTableId).prop('rows')[1]).removeClass('before_searched');
            $($(defaultTableId).prop('rows')[1]).addClass('selected').siblings().removeClass('selected');
            // 처음 refresh이후 선택
            var details_json=$($(defaultTableId).prop('rows')[1]).find('td:nth-child(4)').find('div').html();
            if (!user_function.isEmpty(details_json)) func_automation.gridRowClick(details_json);
        },
        screenshotList: async function(filePath, type) {
            // console.log('screenshotList');
            var result = await service_common.fileList(filePath, type, "", "desc");
            var resultList = JSON.parse(result);
            for (var rowIdx = 0; rowIdx < resultList.length; rowIdx++) {
                var depth1Dir = resultList[rowIdx].depth1Dir;
                var fileCustomDir = resultList[rowIdx].fileCustomDir;
                var localIp =resultList[0].host;

                var imgDir;
                if(localIp == null) {
                    imgDir = '/load-type/' + fileCustomDir;
                } else {
                    imgDir = localIp +"/load-type/" + fileCustomDir
                }
                if( user_modal.val("image.skip") < rowIdx) {
                    $(".grid").append(`<div class='grid-item'><img src='/load-type/${fileCustomDir}' data-original='${imgDir}' /></div>`);
                }
            }
            user_viewer.grid();
        },
    }
})();

