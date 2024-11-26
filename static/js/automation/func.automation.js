var func_automation = func_automation || (function(){
    var console = window.console || {log:function(){},error:function(){},warn:function(){},dir:function(){}};
    console.dir(this.document.currentScript.src);
    return{
        settingData: [],
        SCREENSHOT_FILE_DIR: "screenshot",
        init: function(e){
            console.dir(this.document.currentScript.src);
        },
        gridRowClick: function (fileCustomDir) {
            user_viewer.clean();
            func_automation.selectSceenshotList(func_automation.SCREENSHOT_FILE_DIR+ fileCustomDir, 'fileName');
        },
        selectSettingList: async function(fileDir, type) {
            console.dir('selectSettingList');
            var viewName = "exec";
            var viewNameId = `#${viewName}View`;
            var viewTable = `${viewName}Table`;
            var viewTableId = `#${viewTable}`;

            var result = await user_common.loadType('automation-setting-file-dir');

            if (user_function.isEmpty(result)) {
                $(viewNameId).html("<table id='execTable' class='table no-margin'></table>");
            } else {
                var resultList = JSON.parse(result);
                $(viewNameId).html("<table id='"+viewTable+"' class='table no-margin'></table>");
                $(viewTableId).append(
                    "<thead><tr>"
                    + "<th style='text-align:center; font-size:12px;'>No</th>"
                    + "<th style='text-align:center; font-size:12px;'>실행명</th>"
                    + "<th style='text-align:center; font-size:12px;'>실행</th>"
                    + "</tr></thead>");

                for (var rowIdx = 0; rowIdx < resultList.length; rowIdx++) {
                    var siteName = resultList[rowIdx].siteName;
                    var siteExecName = resultList[rowIdx].siteExecName;
                    var siteExecDesc = resultList[rowIdx].siteExecDesc;
                    var siteUrl = resultList[rowIdx].siteUrl;
                    func_automation.settingData.push({siteExecName: siteExecName, siteExecDesc: siteExecDesc})

                    $(viewTableId).append(
                        "<tr>"
                        + `<td style='text-align:left; font-size:12px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'>${rowIdx+1}</div></td>`
                        + `<td style='text-align:left; font-size:12px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'>${siteExecDesc}</div></td>`
                        + `<td style='text-align:center; font-size:12px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'><a name=${siteExecName} onclick='user_file.pythonExec(${rowIdx});'>실행</a></div></td>`
                        + "</tr>");
                }
            }
        },
        selectLogDirList: async function(fileDir, type) {
            console.dir('selectLogDirList')
            var viewName = "file";
            var viewNameId = `#${viewName}View`;
            var viewTable = `${viewName}Table`;
            var viewTableId = `#${viewTable}`;
            var result = await user_file.fileList(fileDir, type);

            if (user_function.isEmpty(result)) {
                $(viewNameId).html("<table id='execTable' class='table no-margin'></table>");
            } else {
                var resultList = JSON.parse(result);
                $(viewNameId).html(`<table id=${viewTable} class='table no-margin'></table>`);
                $(viewTableId).append(
                    "<thead><tr>"
                    + "<th style='text-align:center; font-size:12px;'>No</th>"
                    + "<th style='text-align:center; font-size:12px;'>실행결과</th>"
                    + "<th style='text-align:center; font-size:12px;'>시간</th>"
                    + "<th style='text-align:center; font-size:12px; display: none;'>param</th>"
                    + "</tr></thead>");

                // 내림차순정렬
                var sortList = user_function.sortDesc(resultList, 'depth3Dir');
                for (var rowIdx = 0; rowIdx < sortList.length; rowIdx++) {
                    var depth2Dir = sortList[rowIdx].depth2Dir;
                    var depth3Dir = sortList[rowIdx].depth3Dir;
                    var varDir = "\\\\" + depth2Dir + "\\\\" + depth3Dir;
                    var displayDir = depth2Dir + "\\" + depth3Dir;
                    var varTime = depth3Dir.split('_')[1];
                    var displayTime = varTime.substring(0, 2) + ":" + varTime.substring(2, 4) + ":" + varTime.substring(4, 6)
                    func_automation.settingData.map(row => {
                        if (row.siteExecName == depth2Dir) displayDir = row.siteExecDesc
                    });

                    $(viewTableId).append(
                        "<tr>"
                        + `<td style='text-align:left; font-size:12px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'>${rowIdx + 1}</div></td>`
                        + `<td style='text-align:left; font-size:12px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'>${displayDir}</div></td>`
                        + `<td style='text-align:left; font-size:12px;'><div style='overflow: hidden; text-overflow: ellipsis; width: 100%; height:20px'>${displayTime}</div></td>`
                        + `<td style='text-align:left; font-size:12px; display: none;'><div>${varDir}</div></td>`
                        + "</tr>"
                    );
                }

                $(viewTableId + " tr").click(function () {
                    // 첫번째줄선택 disabled
                    if ($(this).find('th:first').html() === 'No') return;

                    $(this).removeClass('before_searched');
                    $(this).addClass('selected').siblings().removeClass('selected');

                    var paramData = $(this).find('td:last').find('div').html();
                    func_automation.gridRowClick(paramData)
                });
                $($(viewTableId).prop('rows')[1]).removeClass('before_searched');
                $($(viewTableId).prop('rows')[1]).addClass('selected').siblings().removeClass('selected');
                // 처음 refresh이후 선택
                var details_json2=$($(viewTableId).prop('rows')[1]).find('td:nth-child(4)').find('div').html();
                if (!user_function.isEmpty(details_json2)) clickTableRow2(details_json2);
            }
        },
        selectSceenshotList: async function(fileDir, type) {
            console.dir('selectSceenshotList')
            var result = await user_file.fileList(fileDir, type);
            var resultList = JSON.parse(result);
            for (var rowIdx = 0; rowIdx < resultList.length; rowIdx++) {
                var depth1Dir = resultList[rowIdx].depth1Dir;
                var fileCustomDir = resultList[rowIdx].fileCustomDir;
                var localIp =resultList[0].host;

                var imgDir;
                if(localIp == null) {
                    imgDir = '/loadType/' + fileCustomDir;
                } else {
                    imgDir = localIp +"/loadType/" + fileCustomDir
                }
                if( user_modal.val("image.skip") < rowIdx) {
                    $(".grid").append(`<div class='grid-item'><img src='loadType/${fileCustomDir}' data-original='${imgDir}' /></div>`);
                }
            }
            user_viewer.grid();
        },
    }
})();

