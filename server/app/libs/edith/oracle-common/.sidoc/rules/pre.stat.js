; (function (params) {
    data = params[0]
    result = {}
    result.product = ""
    result.author = ""
    result.customer = ""
    result.datetime = $.ymdhms()
    result.hostid = ""
    result.hosttype = ""
    result.host = {}
    result.hosts = []
    result.hostip = ""
    result.hostips = []
    result.db = {}
    result.db.version = ""
    result.db.id = "X"
    result.id = "X"
    result.db.instances = []
    result.db.size = 0

    if (data.hasOwnProperty("MySQLLog")) {
        result.product = "MySQL"
        try {
            result.author = data["meta"]["author"]["name"]
        }
        catch (err) {
            $.print("result.author", err.message)
        }
        try {
            result.customer = data["meta"]["customer"]
        }
        catch (err) {
            $.print("result.customer", err.message)
        }
        try {
            result.hostid = data["OracleConfs"][0]["host"]["hostId"]
        }
        catch (err) {
            $.print("result.hostid", err.message)
        }
        try {
            result.hosttype = data["MySQLConf"][0]["host"]["os"]
        }
        catch (err) {
            $.print("result.hosttype", err.message)
        }
        try {
            result.host = data["MySQLConf"][0]["host"]
        }
        catch (err) {
            $.print("result.host", err.message)
        }
        try {
            for (i = 0; i < data["SysConfs"].length; i++) {
                result.hosts.push(data["SysConfs"][i]["host"])
            }
        }
        catch (err) {
            $.print("result.hosts", err.message)
        }
        try {
            result.hostip = ""
        }
        catch (err) {
            $.print("result.hostip", err.message)
        }
        try {
            result.hostips = []
        }
        catch (err) {
            $.print("result.hostips", err.message)
        }
        try {
            result.db.version = data["MySQLLog"][0]["basic_information_of_database"][0][0]["Server_version"]
        } catch (err) {
            $.print("result.db.version", err.message)
        }
        try {
            result.db.id = data["MySQLConf"][0]["host"]["hostId"] + "." + data["MySQLConf"][0]["port"]
        }
        catch (err) {
            $.print("result.db.id", err.message)
        }
        try {
            for (i = 0; i < data["MySQLLog"].length; i++) {
                result.db.instances.push(data["MySQLLog"][0]["basic_information_of_database"][0][0])
            }
        }
        catch (err) {
            $.print("result.db.instances", err.message)
        }
        try {
            tbsdata = data["MySQLLog"][0]["all_databases_of_the_current_database_instance_and_their_capacity"][0]
            result.db.size = 0
            for (i = 0; i < tbsdata.length; i++) {
                result.db.size += Number(tbsdata[i]["data_size_mb"])
            }
            result.db.size = Number(result.db.size.toFixed(2))
        }
        catch (err) {
            $.print("result.db.size", err.message)
        }

    } else if (data.hasOwnProperty("OracleConfs")) {
        result.product = "Oracle"
        try {
            result.author = data["meta"]["author"]["name"]
        }
        catch (err) {
            $.print("result.author", err.message)
        }
        try {
            result.customer = data["meta"]["customer"]
        }
        catch (err) {
            $.print("result.customer", err.message)
        }
        try {
            result.hostid = data["OracleConfs"][0]["host"]["hostId"]
        }
        catch (err) {
            $.print("result.hostid", err.message)
        }
        try {
            result.hosttype = data["OracleConfs"][0]["host"]["os"]
        }
        catch (err) {
            $.print("result.hosttype", err.message)
        }
        try {
            result.host = data["OracleConfs"][0]["host"]
        }
        catch (err) {
            $.print("result.host", err.message)
        }
        try {
            for (i = 0; i < data["SysConfs"].length; i++) {
                result.hosts.push(data["SysConfs"][i]["base"])
            }
        }
        catch (err) {
            $.print("result.hosts", err.message)
        }
        try {
            if (data["OracleConfs"][0]["host"].hasOwnProperty("\tIP Address")) {
                result.hostip = data["OracleConfs"][0]["host"]["\tIP Address"] // AIX
            } else {
                result.hostip = data["OracleConfs"][0]["host"]["IP address"]
            }
        }
        catch (err) {
            $.print("result.hostip", err.message)
        }
        try {
            for (i = 0; i < data["SysConfs"].length; i++) {
                thisips = data["SysConfs"][i]["base"]["IP address"].split(" ")
                for (j = 0; j < thisips.length; j++) {
                    result.hostips.push(thisips[j])
                }
            }
        }
        catch (err) {
            $.print("result.hostips", err.message)
        }
        try {
            result.db.version = data["OracleConfs"][0]["instance"]["dbversion"]
        } catch (err) {
            $.print("result.db.version", err.message)
        }
        try {
            result.db.id = data["OracleConfs"][0]["instance"]["cluster"]
        }
        catch (err) {
            $.print("result.db.id", err.message)
        }
        try {
            for (i = 0; i < data["OracleConfs"].length; i++) {
                result.db.instances.push(data["OracleConfs"][i]["instance"])
            }
        }
        catch (err) {
            $.print("result.db.instances", err.message)
        }
        try {
            tbsdata = data["OracleStatus"][0]["tbscheck"][0]["metric"]
            if (!tbsdata) {
                tbsdata = data["OracleStatus"][0]["tbscheck12c"][0]["metric"]
            }
            for (i = 0; i < tbsdata.length; i++) {
                result.db.size += Number(tbsdata[i]["used"])
            }
        }
        catch (err) {
            $.print("result.db.size", err.message)
        }

    } else if (data.hasOwnProperty("SysConfs")) {
        if (data["SysConfs"][0].hasOwnProperty("ip")) {
            result.product = "OS"
            try {
                result.author = data["meta"]["author"]["name"]
            }
            catch (err) {
                $.print("result.author", err.message)
            }
            try {
                result.customer = data["meta"]["customer"]
            }
            catch (err) {
                $.print("result.customer", err.message)
            }
            try {
                result.hostid = data["SysConfs"][0]["host"]["hostId"]
            }
            catch (err) {
                $.print("result.hostid", err.message)
            }
            try {
                result.hosttype = data["SysConfs"][0]["host"]["os"]
            }
            catch (err) {
                $.print("result.hosttype", err.message)
            }
            try {
                result.host = data["SysConfs"][0]["host"]
            }
            catch (err) {
                $.print("result.host", err.message)
            }
            try {
                for (i = 0; i < data["SysConfs"].length; i++) {
                    result.hosts.push(data["SysConfs"][i]["base"])
                }
            }
            catch (err) {
                $.print("result.hosts", err.message)
            }
            try {
                if (data["OracleConfs"][0]["host"].hasOwnProperty("\tIP Address")) {
                    result.hostip = data["OracleConfs"][0]["host"]["\tIP Address"] // AIX
                } else {
                    result.hostip = data["OracleConfs"][0]["host"]["IP address"]
                }
            }
            catch (err) {
                $.print("result.hostip", err.message)
            }
            try {
                for (i = 0; i < data["SysConfs"].length; i++) {
                    thisips = data["SysConfs"][i]["base"]["IP address"].split(" ")
                    for (j = 0; j < thisips.length; j++) {
                        result.hostips.push(thisips[j])
                    }
                }
            }
            catch (err) {
                $.print("result.hostips", err.message)
            }
            try {
                result.db.version = data["OracleConfs"][0]["instance"]["dbversion"]
            } catch (err) {
                $.print("result.db.version", err.message)
            }
            try {
                result.db.id = data["OracleConfs"][0]["instance"]["cluster"]
            }
            catch (err) {
                $.print("result.db.id", err.message)
            }
            try {
                for (i = 0; i < data["OracleConfs"].length; i++) {
                    result.db.instances.push(data["OracleConfs"][i]["instance"])
                }
            }
            catch (err) {
                $.print("result.db.instances", err.message)
            }
            try {
                tbsdata = data["OracleStatus"][0]["tbscheck"][0]["metric"]
                if (!tbsdata) {
                    tbsdata = data["OracleStatus"][0]["tbscheck12c"][0]["metric"]
                }
                for (i = 0; i < tbsdata.length; i++) {
                    result.db.size += Number(tbsdata[i]["used"])
                }
            }
            catch (err) {
                $.print("result.db.size", err.message)
            }
        }
    }

    if (result.hostips.length == 0 && result.hostip) {
        result.hostips.push(result.hostip)
    }

    if (result.hostips.length != 0 && !result.hostip) {
        result.hostip = result.hostips[0]
    }

    //tojson(result)
    result.id = result.db.id
    return result
})(input)