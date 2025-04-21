class SaveLoad{

    constructor(sys_control){
        this.sys_control = sys_control;
    }

    getSaveData(){
        const result = {}

        result["Record"] = this.sys_control.mainRecoardCenterProccess.mainData;
        result["StartKey"] = this.sys_control.mainRecoardCenterProccess.startKey;

        const saveText = JSON.stringify(result,
            (key, value) => typeof value === "bigint" ? value.toString().padStart(64, '0') : value,
            2);

        return saveText;
    }

    Load(jsonString){

        //エラーチェックはする。あとで。

        
        
        // BigIntを復元するための関数付きJSON.parse
        const regex = new RegExp('^[0-9]+');
        const restoredData = JSON.parse(jsonString, (key, value) =>
            typeof value === "string" && regex.test(value) && value.length > 15 // BigIntの可能性
            ? BigInt(value)
            : value
        );
        


        //問題なければ代入
        this.sys_control.mainRecoardCenterProccess.mainData = restoredData["Record"];
        this.sys_control.mainRecoardCenterProccess.startKey = restoredData["StartKey"];

        this.sys_control.mainRecoardCenterProccess.nowUuid = restoredData["StartKey"];


        this.sys_control.guiControl.mainRecordSelectIndex = 0;//本譜のセレクトボックスの一番上を選択させる
        
        const aaa=9;
    }
}