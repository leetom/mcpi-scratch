(function (ext) {

    var ext_url = "http://www.codepku.com/scratch/ext/mcpi-scratch.js";

    var blockHits = false;
    var server_host = "http://mc.codepku.com";
    var server_port = 4715;

    var request_timeout = 4000;

    var request_frequency = 4; //每秒限制5次请求，防止服务器端负载过高。


    var server_url = server_host + ":" + server_port;

    var READY = false;

    ext.checkReady = function(){
        return READY;
    }

    //检查是否请求超过频率限制。
    ext.checkOverclock = function(count){
        var count = count === undefined ? true : count;
        var timestamp = Math.floor((new Date).getTime() / 1000);
        if(ext._status.freq_time == timestamp){
            if(count){  //这次调用是否计数
                ext._status.freq_count++;
            }
        }else{
            ext._status.freq_time = timestamp;
            ext._status.freq_count = 0;
        }

        if(ext._status.freq_count > request_frequency){
            return true;
        }

        return false;
    }

    ext.userName = function(){
        if($('.user-name')){
            return $('.user-name a').text().trim();
        }else{
            return '';
        }
    }

    if(ext.userName()){
        server_url += "/" + ext.userName(); //用户名作为参数传递
    }

    ext.postToChat = function(str) {
        if(!ext.checkReady() || ext.checkOverclock(false)) return;
        console.log(str);
        console.log(document.cookie);
        console.log($('.user-name').text());
        var cmdUrl = server_url + "/postToChat/" + encodeURIComponent(str);
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("postToChat success");
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error postToChat: ", error);
            }
        }); // nb: GET is including the javascript callback. Do I need this for one-way call?
    };

    ext.playerPosToChat = function() {
        if(!ext.checkReady() || ext.checkOverclock()) return;
        var cmdUrl = server_url + "/playerPosToChat";
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            // dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("playerPosToChat success");
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error playerPosToChat: ", error);
            }
        }); // nb: GET is including the javascript callback. Do I need this for one-way call?
    };

    ext.setPlayerPos = function(x, y, z) {
        if(!ext.checkReady() || ext.checkOverclock()) return;
        var cmdUrl = server_url + "/setPlayerPos/" + x + "/" + y + "/" + z;
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("setPlayerPos success");
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error setPlayerPos: ", error);
            }
        }); // nb: GET is including the javascript callback. Do I need this for one-way call?
    };

    ext.setBlock = function(x, y, z, blockType, blockData, posType) {
        if(!ext.checkReady() || ext.checkOverclock()) return;
        var cmdUrl = server_url + "/setBlock/" + x + "/" + y + "/" + z + "/" + blockType + "/" + blockData + "/" + posType;
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("setBlock success");
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error setBlock: ", error);
            }
        }); // nb: GET is including the javascript callback. Do I need this for one-way call?
    };

    ext.setBlocks = function(x1, y1, z1, x2, y2, z2, blockType, blockData) {
        if(!ext.checkReady() || ext.checkOverclock()) return;
        var cmdUrl = server_url + "/setBlocks/" + x1 + "/" + y1 + "/" + z1 + "/" 
            + x2 + "/" + y2 + "/" + z2 + "/" + blockType + "/" + blockData;
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("setBlocks success");
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error setBlocks: ", error);
            }
        }); // nb: GET is including the javascript callback. Do I need this for one-way call?
    };

    ext.setLine = function(x1, y1, z1, x2, y2, z2, blockType, blockData) {
        if(!ext.checkReady() || ext.checkOverclock()) return;
        var cmdUrl = server_url + "/setLine/" + x1 + "/" + y1 + "/" + z1 + "/"
            + x2 + "/" + y2 + "/" + z2 + "/" + blockType + "/" + blockData;
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("setLine success");
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error setLine: ", error);
            }
        }); // nb: GET is including the javascript callback. Do I need this for one-way call?
    };

    ext.setCircle = function(x, y, z, r, blockType, blockData, horizontal = false) {
        if(!ext.checkReady() || ext.checkOverclock()) return;
        var cmd = horizontal ? "/setHCircle/" : "/setCircle/";
        var cmdUrl = server_url + cmd + x + "/" + y + "/" 
            + z + "/" + r + "/" + blockType + "/" + blockData;
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("setCircle success");
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error setCircle: ", error);
            }
        }); // nb: GET is including the javascript callback. Do I need this for one-way call?
    };

    ext.setHCircle = function(x, y, z, r, blockType, blockData) {
       ext.setCircle(x, y, z, r, blockType, blockData, true);
    };

    ext.setSphere = function(x, y, z, r, blockType, blockData) {
        if(!ext.checkReady() || ext.checkOverclock()) return;

        var cmdUrl = server_url + "/setSphere/" + x + "/" + y + "/" 
            + z + "/" + r + "/" + blockType + "/" + blockData;
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("setSphere success");
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error setSphere: ", error);
            }
        }); // nb: GET is including the javascript callback. Do I need this for one-way call?
    };

    ext.setText = function(str, x, y, z, blockType, blockData){
        if(!ext.checkReady() || ext.checkOverclock()) return;

        var cmdUrl = server_url + "/setText/" + str + "/" + x + "/" + y + "/" 
            + z + "/" + blockType + "/" + blockData;
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("setText success");
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error setText: ", error);
            }
        });
    }

    // get one coord (x, y, or z) for playerPos
    ext.getPlayerPos = function(posCoord, callback) {
        if(!ext.checkReady() || ext.checkOverclock()) return;
        var cmdUrl = server_url + "/getPlayerPos/" + posCoord;
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("getPlayerPos success ", data.trim());
                callback(data.trim());
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error getPlayerPos: ", error);
                callback(null);
            }
        }); 
    };

    // get one coord (x, y, or z) for playerPos
    ext.getBlock = function(x, y, z, posType, callback) {
        if(!ext.checkReady() || ext.checkOverclock()) return;
        var cmdUrl = server_url + "/getBlock/" + x + "/" + y + "/" + z + "/" + posType;
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("getPlayerPos success ", data.trim());
                callback(data.trim());
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error getPlayerPos: ", error);
                callback(null);
            }
        }); 
    };

    function checkMC_Events() {
        if(!ext.checkReady() || ext.checkOverclock()) return;
        var cmdUrl = server_url + "/pollBlockHit/";
        $.ajax({
            timeout: request_timeout,
            type: "POST",
            url: cmdUrl,
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("checkMC_Events success ", data.trim());
                if (parseInt(data) == 1)
                    blockHits = true;
                else
                    blockHits = false;
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                console.log("Error checkMC_Events: ", error);
                callback(null);
            }
        }); 
    };

    ext.whenBlockHit = function(str) {
        if(!ext.checkReady()) return;
        if (!blockHits)
            return;
        else
            return true;
    };


    ext._status = {
        success: {status: 2, msg:'Ready' },
        waiting: {status: 1, msg: '请加入MC服务器'},
        need_login: {status: 0, msg: '登录之后才能使用'},
        last_ready_time: (new Date).getTime(),  //上次确认ready的时间（毫秒）
        last_check_time: (new Date).getTime(),  //上次到服务器上查询的时间（限制2秒一次）
        //频率限制
        frequency: {status: 1, msg: '请求速度过快，请在循环中加入等待时间'},
        freq_time: Math.floor((new Date).getTime() / 1000),
        freq_count: 0,

    };


    ext._getStatus = function() {
        console.log('_getStatus');
        if(ext.userName() == ''){
            return ext._status.need_login;
        }
        if(ext.checkOverclock(false)){
            return ext._status.frequency;
        }
        //5s 之内检查过 ready
        if(ext.checkReady() && (new Date).getTime() - ext._status.last_ready_time < 5000) 
            return ext._status.success;

        if((new Date).getTime() - ext._status.last_check_time < 2000 )
            return ext._status.waiting;
        var cmdUrl = server_url + "/checkReady/";
        $.ajax({
            timeout: request_timeout + 1000,    //checkready 等待时间长一点
            type: "GET",
            url: cmdUrl,
            // async: false,   // 需要异步，否则Scratch的SWF会卡住。
            //dataType: "jsonp", // hack for the not origin problem - replace with CORS based solution
            success: function(data) {
                console.log("mc server ready " + data.trim());
                returnData = data.trim();
                if(data.trim() == 'true'){
                    console.log("ready");
                    READY = true;
                    ext._status.last_ready_time = (new Date).getTime();
                }else{
                    READY = false;
                }
            },
            error: function(jqxhr, textStatus, error) { // have to change this coz jasonp parse error
                READY = false;
                console.log("mc server failed ", error);
            },
        }); 
        ext._status.last_check_time = (new Date).getTime();
        // 刚检查过了暂时为上次的状态
        return READY ? ext._status.success : ext._status.waiting;
    };

    ext._shutdown = function() {
        if (poller) {
          clearInterval(poller);
          poller = null;
        }
    };

    // Block and block menu descriptions
    var descriptor = {
        blocks: [
            ['', 'post to chat %s', 'postToChat', 'message'],
            [" ", "post Player.pos chat", "playerPosToChat"],
            [" ", "set Player pos to x:%n y:%n z:%n", "setPlayerPos", 0, 0, 0],
            [" ", "set block pos x:%n y:%n z:%n to type %n data %n %m.blockPos", "setBlock", 0, 0, 0, 1, -1],
            [" ", "set blocks pos x1:%n y1:%n z1:%n to x2:%n y2:%n z2:%n to type %n data %n", "setBlocks", 0, 0, 0, 0, 0, 0, 1, -1],
            [" ", "set line from x1:%n y1:%n z1:%n to x2:%n y2:%n z2:%n to type %n data %n", "setLine", 0, 0, 0, 0, 0, 0, 1, -1],
            [" ", "set circle center x1:%n y1:%n z1:%n radius r:%n to type %n data %n", "setCircle", 0, 0, 0, 0, 1, -1],
            [" ", "set horizontal circle center x1:%n y1:%n z1:%n radius r:%n to type %n data %n", "setHCircle", 0, 0, 0, 0, 1, -1],
            [" ", "set sphere center at x1:%n y1:%n z1:%n radius r:%n to type %n data %n", "setSphere", 0, 0, 0, 0, 1, -1],
            [" ", "set text %s at x1:%n y1:%n z1:%n with type %n data %n", "setText", "Hello", 0, 0, 0, 1, -1],
            ["R", "get player pos %m.pos", "getPlayerPos", 'x'],
            ["R", "get block pos x:%n y:%n z:%n %m.blockPos", "getBlock", 0, 0, 0],
            ["h", "when blockHit", 'whenBlockHit'],
        ],
        menus: {
            pos: ['x', 'y', 'z'],
            blockPos: ['abs', 'rel']
        }
    };

    // Register the extension
    ScratchExtensions.register('编玩Craft-Scratch', descriptor, ext);

    checkMC_Events();
    var poller = setInterval(checkMC_Events, 3000);

})({});
