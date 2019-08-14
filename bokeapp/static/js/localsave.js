
var storage = window.localStorage;

function save() {
    //alert("test");
    var boke = '1234315521';
    console.log(boke);
        if (!boke){
            storage.setItem("key", boke)
        }
        if(boke){
        var temp = storage.getItem('key');
            boke.write(temp)
        }
}
function clear() {
    storage.clear();
}


var t1 = window.setTimeout("save()", 10000);
var t2 = window.setTimeout("clear()",9000);