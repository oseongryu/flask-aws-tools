var user_function = user_function || (function(){
	var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    // console.log(this.document.currentScript.src);
	return{
        init: function(e){
            console.log(this.document.currentScript.src);
        },
        pad: function(number, length){
          var str = '' + number;
          while(str.length < length){
              str= '0' + str;
          }
          return str;
        },
        dateToDateTimeString: function(now){
            var year = now.getFullYear().toString();
            var month = user_function.pad(now.getMonth()+1, 2).toString();
            var day = user_function.pad(now.getDate(),2).toString();
            var hours = user_function.pad(now.getHours(),2).toString();
            var minutes  = user_function.pad(now.getMinutes(),2).toString();
            var seconds  = user_function.pad(now.getSeconds(),2).toString();
            return year+'-'+month+'-'+day +' ' + hours + ':' + minutes + ':' + seconds;
        },
        dateToString : function(nowDate){
            var year = nowDate.getFullYear().toString();
            var month = user_function.pad(nowDate.getMonth()+1, 2).toString();
            var day = user_function.pad(nowDate.getDate(),2).toString();
            return year+month+day;
        },
        dateToDynamoDate : function(searchDate){
            var year = searchDate.substring(0,4);
            var month = user_function.numToMonth(searchDate.substring(4,6));
            var day = searchDate.substring(6,8);
            return day+ '/'+ month + '/'+ year;
        },
        numToMonth : function(num){
            var val = "";
            switch(num){
                case "01": val = "Jan"; break;
                case "02": val = "Feb"; break;
                case "03": val = "Mar"; break;
                case "04": val = "Apr"; break;
                case "05": val = "May"; break;
                case "06": val = "Jun"; break;
                case "07": val = "Jul"; break;
                case "08": val = "Aug"; break;
                case "09": val = "Sep"; break;
                case "10": val = "Oct"; break;
                case "11": val = "Nov"; break;
                case "12": val = "Dec"; break;
            }
            return val;
        },
        isEmpty: function(obj) {
            // https://sanghaklee.tistory.com/3
            if (obj == ""
             || obj == null
             || obj == undefined
             || (obj != null && typeof obj == "object" && !Object.keys(obj).length)) {
                return true;
            } else {
                return false;
            }
        },
        sort: function(obj, value, type) {
            var result;
            if (type == 'desc') {
                result = user_function.sortDesc(obj, value);
            } else if(type == 'asc') {
                result = user_function.sortAsc(obj, value);
            }
            return result;
        },
        sortDesc: function(obj, value) {
            var result = obj.sort(function(a, b) {
                var caseA = a[value];
                var caseB = b[value];
                if(caseA < caseB) return 1;
                if(caseA > caseB) return -1;
                if(caseA === caseB) return 0;
            });
            return result;
        },
        sortAsc: function(obj, value) {
            var result = obj.sort(function(a, b) {
                var caseA = a[value];
                var caseB = b[value];
                if(caseA > caseB) return 1;
                if(caseA < caseB) return -1;
                if(caseA === caseB) return 0;
            });
            return result;
        },
	}
})();

