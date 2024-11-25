var user_json = user_json || (function(){
	var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    console.dir(this.document.currentScript.src);
	return{
        init: function(e){
            console.dir(this.document.currentScript.src);
        },
        // https://stackoverflow.com/questions/19098797/fastest-way-to-flatten-un-flatten-nested-json-objects
        flatten: function(data) {
            var result = {};
            function recurse (cur, prop) {
                if (Object(cur) !== cur) {
                    result[prop] = cur;
                } else if (Array.isArray(cur)) {
                     for(var i=0, l=cur.length; i<l; i++)
                         recurse(cur[i], prop ? prop+"."+i : ""+i);
                    if (l == 0)
                        result[prop] = [];
                } else {
                    var isEmpty = true;
                    for (var p in cur) {
                        isEmpty = false;
                        recurse(cur[p], prop ? prop+"."+p : p);
                    }
                    if (isEmpty)
                        result[prop] = {};
                }
            }
            recurse(data, "");
            return result;
        },
        unflatten: function(data) {
            "use strict";
            if (Object(data) !== data || Array.isArray(data))
              return data;
            var result = {}, cur, prop, idx, last, temp;
            for(var p in data) {
              cur = result, prop = "", last = 0;
              do {
                  idx = p.indexOf(".", last);
                  temp = p.substring(last, idx !== -1 ? idx : undefined);
                  cur = cur[prop] || (cur[prop] = (!isNaN(parseInt(temp)) ? [] : {}));
                  prop = temp;
                  last = idx + 1;
              } while(idx >= 0);
              cur[prop] = data[p];
            }
            return result[""];
        },
        getDepthJsonData: function (obj, data) {
            var returnVal = "";

            if(user_function.isEmpty(obj)){
                returnVal =  data
            } else {
                var splitData = obj.split('.');
                if (splitData.length == 1) {
                    returnVal =  data[splitData[0]];
                    if(returnVal == undefined) {
                        returnVal = data
                    }

                } else if (splitData.length == 2) {
                    returnVal =  data[splitData[0]][splitData[1]];
                    if(returnVal == undefined) {
                       returnVal = data
                    }
                } else if (splitData.length == 3) {
                    returnVal =  data[splitData[0]][splitData[1]][splitData[2]];
                    if(returnVal == undefined) {
                        returnVal = data
                    }
                } else if (splitData.length == 4) {
                   returnVal =  data[splitData[0]][splitData[1]][splitData[2]][splitData[3]];
                   if(returnVal == undefined) {
                       returnVal = data
                   }
                }
                else {
                    returnVal = data;
                }
            }
            return returnVal;
        },
        getDepthJsonData2: function (obj, data, number) {
         var returnVal = "";
         if(!user_function.isEmpty(obj)){
            if(number > 0){
               returnVal =  data[splitData[0]];
               if(returnVal == undefined) {
                    returnVal = data
               }else{
                    getDepthJsonData(obj, returnVal, number -1)
               }
            } else {
               returnVal =  data[splitData[0]];
               if(returnVal == undefined) {
                    returnVal = data
               }
            }
         } else {
             returnVal =  data
         }
         return returnVal;
        },
        getDepth: function (obj) {
            var depth = 0;
            if (obj.children) {
                obj.children.forEach(function (d) {
                    var tmpDepth = getDepth(d)
                    if (tmpDepth > depth) {
                        depth = tmpDepth
                    }
                })
            }
            return 1 + depth
        },
        // https://techtutorialsx.com/2021/04/02/javascript-obtaining-object-depth/
        getObjectDepth: function (obj) {
            if (typeof obj !== "object" || obj === null) {
                return 0;
            }
            const flat = this.flatten(obj);
            const keys =  Object.keys(flat);

            let deepest = {
                depth: 1,
                key: null,
                value: null
            };
            if(keys.length === 0){
                return deepest;
            }
            for(let key of keys){
                const length = key.split(".").length;
                if(length > deepest.depth){
                    deepest = {
                        depth: length,
                        key: key,
                        value: flat[key]
                    }
                }
            }
            return deepest;
        },
        getVal: function (obj, key) {
            var flattenData = user_json.flatten(obj);
            var arrList = []

            Object.keys(flattenData).map(row=> {
                arrList.push(row)
            });
            var val = "";
            for (var rowIndex= 0; rowIndex < arrList.length; rowIndex++){
                try {
                    // 설정값 skip
                    var settingKey = arrList[rowIndex];
                    var settingVal = sessionStorage.getItem(arrList[rowIndex]);
                    if(!user_function.isEmpty(settingVal) && settingKey == key) {
                        val = settingVal;
                        break;
                    }
                } catch(e){
                }
            }
            return val;
        }
	}
})();

