class CpuLevelSetting{
    constructor(add_lie,deep_num){
        this.add_lie = add_lie;
        this.deep_num =deep_num;
        
    }

}

class SystemControl{
    constructor(){
        //棋譜データのクラス
        this.mainRecoardCenterProccess = null;

        //盤面の表示のコントロール用
        this.mainBoard = null;
            
        //盤面のデータ
        this.mainReversiGame=null;

        //通信エラー等でゲームを停止させるフラグ
        this.isErrorStop = false;

        //CPUが打つ手番
        this.isFirstCpuFlag = false;
        this.isSecondCpuFlag = true;

        this.isPossiblePlayerMove = true;//盤面をクリック可能かどうか

        //cpu思考中ならtrue
        this.cpuNowThinking = false;
        
        this.deep_num = 1;//深読み手数
        this.add_lie = 0.0//ランダム量

        //カスタム以外のCPUのプリセット

        this.cpu_level_data={
            "easy":new CpuLevelSetting(1000,1),
            "normal":new CpuLevelSetting(100,1),
            "hard":new CpuLevelSetting(10,1),
            "yuutesonnnatuyokunai":new CpuLevelSetting(5,3)
        };

        this.isGamePlaying = false ;
        this.isConsiderScreen = true;//検討画面にいるときtrue
    }

    setClassData(mainRecoardCenterProccess,mainBoard,mainReversiGame,saveLoad,guiControl,reversiSendReceive){
        //棋譜データのクラス
        this.mainRecoardCenterProccess = mainRecoardCenterProccess;

        //盤面の表示のコントロール用
        this.mainBoard = mainBoard;
            
        //盤面のデータ
        this.mainReversiGame = mainReversiGame;

        this.guiControl = guiControl;

        this.reversiSendReceive = reversiSendReceive;

        this.saveLoad = saveLoad;

    }

    setCpuLevel(nameString){
        this.deep_num = this.cpu_level_data[nameString].deep_num;
        this.add_lie = this.cpu_level_data[nameString].add_lie;
    }
}

