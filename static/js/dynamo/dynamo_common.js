function onClickDynamo() {
    prev_epoch_uuid = $("#analysisTable").find('td:nth-child(4)').find('div').html();
    var _dynamoDate = user_function.dateToDynamoDate($('#date').val());
    var _tableName = $('#tableName').val();

    sessionStorage.setItem('tableName', _tableName );

    $.ajax({
        url : "/api/dynamo/selectDynamoList",
        method : "POST",
        data : {
            tableName : _tableName,
            date: _dynamoDate
        },
        error : function(result){
            alert('error');
            $("#analysisView").html("<table id='analysisTable' class='table no-margin'></table>");
        },
        success : function(result) {
            refreshList(result);
        }
    });
}

function onClickDynamoQuery() {
    prev_epoch_uuid = $("#analysisTable").find('td:nth-child(4)').find('div').html();
    var _query = $('#query').val();

    sessionStorage.setItem('query', _query);

    $.ajax({
        url : "/api/dynamo/selectDynamoListQuery",
        method : "POST",
        data : {
            query: _query
        },
        error : function(result){
            alert('error');
            $("#analysisView").html("<table id='analysisTable' class='table no-margin'></table>");
        },
        success : function(result) {
            refreshList(result);
        }
    });
}

function clickTableRow(details_json) {
    var data = JSON.parse(details_json);
    var jsonView1Json = user_json.getDepthJsonData($('#view1Text').val(), data);
    $("#jsonView1").html("<pre>"+ JSON.stringify(jsonView1Json, null, 4)+ "</pre>");
    var jsonView2Json = user_json.getDepthJsonData($('#view2Text').val(), data);
    $("#jsonView2").html("<pre>"+ JSON.stringify(jsonView2Json, null, 4)+ "</pre>");
    var jsonView3Json = user_json.getDepthJsonData($('#view3Text').val(), data);
    $("#jsonView3").html("<pre>"+ JSON.stringify(jsonView3Json, null, 4)+ "</pre>");

    var jsonViewOSJson = user_json.getDepthJsonData($('#viewOSText').val(), data);
    $("#jsonViewOS").html("<pre>"+ JSON.stringify(jsonViewOSJson, null, 4)+ "</pre>");
}

function clickTableRow2(paramPath) {
    user_viewer.clean();
    func_automation.selectSceenshotList(func_automation.SCREENSHOT_FILE_DIR+ paramPath, 'fileName');
}

function checkUrl() {
    const href = window.location.href;
    return href.includes('dynamoIndex'); // Returns true if 'dynamoIndex' is present
}

function refreshList(result){
    $("#analysisView").html("<table id='analysisTable' class='table no-margin'></table>");
    $("#analysisTable").append("<thead><tr>"
                                    + "<th style='text-align:center'>ID</th>"
                                    + "<th style='text-align:center'>Date</th>"
                                    + "<th style='te-align:center'>epoch</th>"
                                    + "<th style='text-align:center'>epoch_uuid</th>"
                                    + "<th style='text-align:center'>details_json</th>"
                                    + "</tr></thead>");


    var osDataCnt = 0;
    for (var rowIdx = 0; rowIdx < result.length; rowIdx++) {
        var id = result[rowIdx].id;
        var epoch = result[rowIdx].epoch;
        var epoch_uuid = result[rowIdx].epoch_uuid;
        var date = result[rowIdx].date;
        var details = result[rowIdx].details;
        var details_json = result[rowIdx].details_json;

        var flattenData = user_json.flatten(user_modal.settingData);
        var arrList = []
        Object.keys(flattenData).map(key=> {arrList.push(key)})

        var isEqualText = 0
        for (var rowIdxY= 0; rowIdxY < arrList.length; rowIdxY++){
            try {
                var tempData = user_json.getDepthJsonData(arrList[rowIdxY], JSON.parse(details_json));
                var settingVal = sessionStorage.getItem(arrList[rowIdxY]);
                if(user_function.isEmpty(settingVal)){
                    isEqualText += 1
                }
                else if(tempData === settingVal) {
                    isEqualText += 1
                }
            } catch(e){
                isEqualText +=1
            }
        }

        if(isEqualText == arrList.length) {
            osDataCnt += 1;
            $("#analysisTable").append("<tr>"
                                    + "<td style='text-align:center'>"+ osDataCnt + "</td>"
                                    + "<td style='text-align:center'>"+ date + "</td>"
                                    + "<td style='text-align:center'>"+ epoch + "</td>"
                                    + "<td style='text-align:center'><div style='overflow: hidden; text-overflow: ellipsis; width: 50px; height:20px'>"+ epoch_uuid + "</div></td>"
                                    + "<td style='text-align:center'><div style='overflow: hidden; text-overflow: ellipsis; width: 50px; height:20px'>"+ details_json + "</div></td>"
                                    + "</tr>");
        }
    }
    $('#analysisViewTitle').html("<h3 class='box-title' id='analysisViewTitle'>List ( "+osDataCnt+" )</h3>");

    cur_epoch_uuid = $("#analysisTable").find('td:nth-child(4)').find('div').html();

    var rowCnt = $("#analysisTable").prop('rows').length;
    for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
        var temp_epoch_uuid = $("#analysisTable").prop('rows')[rowIdx].cells[3].innerText;
        if(temp_epoch_uuid === prev_epoch_uuid){
            $('#analysisViewTitle').append( ' / plus: '+ (rowIdx -1))
            $("#analysisTable").prop('rows')[rowIdx].classList.add('before_searched')
            break;
        }
    }

    $("#analysisTable tr").click(function(){
        if($(this).find('th:first').html() === 'ID') return;
        $(this).removeClass('before_searched');
        $(this).addClass('selected').siblings().removeClass('selected');
        var epoch_uuid=$(this).find('td:nth-child(4)').find('div').html();
        var details_json=$(this).find('td:nth-child(5)').find('div').html();
        clickTableRow(details_json);
    });

    // 처음 refresh이후 선택
    $($("#analysisTable").prop('rows')[1]).removeClass('before_searched');
    $($("#analysisTable").prop('rows')[1]).addClass('selected').siblings().removeClass('selected');
    var details_json=$($("#analysisTable").prop('rows')[1]).find('td:nth-child(5)').find('div').html();
    if (!user_function.isEmpty(details_json)) clickTableRow(details_json);
    $('#search_result').text(user_function.dateToDateTimeString(new Date()) + ' search')
}