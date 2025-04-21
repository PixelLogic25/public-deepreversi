class ElementData{
    constructor(element,game_start_hide){
        this.element = element;
        this.game_start_hide = game_start_hide;
    }


}

class ElementCenter{
    constructor(){
        const registerElementData =[
            ["ask-ai-button"                ,false],
            ["selectbox-main-record"        ,true],
            ["main-record-label"            ,true],
            ["selectbox-branch-record"      ,true],
            ["branch-record-label"          ,true],
            ["cpu-level-custom-label"       ,true],
            ["cpu-level-custom-select"      ,true],
            ["is-frist-cpu-checkBox"        ,true],
            ['is-second-cpu-checkBox'       ,true],
            ['game-start-button'            ,true],
            ["file-label"                   ,true],
            ["save-button"                  ,true],
            ["load-button"                  ,true],
            ["game-stop-button"             ,true],
            ["is-frist-cpu-checkBox-label"  ,true],
            ["is-second-cpu-checkBox-label" ,true],
            ["cpu-option-deep-num"          ,false],
            ["cpu-option-add_lie"           ,false],
            ["cpu-custom-close-button"      ,false],
            ["hide-main-content"            ,false],
            ["cpu-level-custom-screen"      ,false],
            ["selected-cpu-custom"          ,false],
            ["file-textarea"                ,true],
            ["game-previos-move-button"     ,true]
        ];
        this.registerElements = {};

        //要素代入
        for(let i=0;  i<registerElementData.length;i++){
            const key = registerElementData[i][0];
            this.registerElements[key] = new ElementData(document.getElementById(key),registerElementData[i][1]);
        }
    };

    get(name){
        return this.registerElements[name].element;
    }
    isGamePlayHideElement(name){
        return this.registerElements[name].game_start_hide;
    }
}


class GuiControl{

     //htmlが読み込まれるときに読まれる
    constructor(sys_control){
        //データのやり取りをするクラスを保持
        this.sys_control = sys_control;

        //盤面の表示のコントロール用
        this.mainBoard = sys_control.mainBoard;
        
        //盤面のデータ
        this.mainReversiGame=sys_control.mainReversiGame;


        //操作する要素を取得する
        this.elements = new ElementCenter();

        //CPU強さのセレクトボックス取得
        //this.cpuLevelSelectboxElements = document.querySelectorAll('.cpu-custom');
        this.cpuLevelSelectbox=this.elements.get("cpu-level-custom-select");

        //本譜の記録のselectbox取得
        this.mainSelectElement = this.elements.get('selectbox-main-record');
        // イベントリスナーを追加
        this.mainSelectElement.addEventListener('change', (event) => {
            // 選択されたオプションのvalueを取得
            const selectedValue = event.target.value;
            this.sys_control.mainRecoardCenterProccess.mainSelect(selectedValue);//本譜select更新

            this.updateBranchSelectElement();//分岐セレクトボックス更新

            //石の個数更新
            this.updateCountStone(this.sys_control.mainRecoardCenterProccess.game.getBlackStouneCount(),this.sys_control.mainRecoardCenterProccess.game.getWhiteStouneCount());
            
            //手番の表示を更新
            this.update_now_turn_display(this.sys_control.mainRecoardCenterProccess.game.board.turn);
        });
       
        this.mainSelectElement.innerHTML = ''; // 本譜のすべての項目を削除

        this.mainRecordSelectIndex = -1;//ここに本譜の選択位置を入れる

        //分岐の選択をselectboxを取得
        this.branchSelectElement = this.elements.get('selectbox-branch-record');

        //選択を変更されたときのイベントリスナーを登録
        this.branchSelectElement.addEventListener('change', (event) => {
            // 選択されたオプションのvalueを取得
            const selectedValue = event.target.value;

            if (selectedValue in this.sys_control.mainRecoardCenterProccess.mainData ){
                this.sys_control.mainRecoardCenterProccess.branchSelect(selectedValue);//分岐の選択をした時の処理
                

                const select_value = this.sys_control.mainRecoardCenterProccess.mainData[this.sys_control.mainRecoardCenterProccess.nowUuid].turn_num;
                this.mainRecordSelectIndex = select_value;
                this.updateSelectElement();
            }
        });
        //this.updateSelectElement();

        //CPUの先手後手のチェックボックス取得
        this.isFristCpuCheckBox = this.elements.get('is-frist-cpu-checkBox');
        this.isFristCpuCheckBox.addEventListener('change', (event) =>{
            this.sys_control.isFirstCpuFlag = this.isFristCpuCheckBox.checked;
        });
        this.isSecondCpuCheckBox = this.elements.get('is-second-cpu-checkBox');
        this.isSecondCpuCheckBox.addEventListener('change', (event) =>{
            this.sys_control.isSecondCpuFlag = this.isSecondCpuCheckBox.checked;
        });


        //対戦開始ボタンの取得
        this.gameStartbutton = this.elements.get('game-start-button');
        this.gameStartbutton.addEventListener('click', (event) =>{


            this.toggleClassGameStart();//GUIの表示非表示切り替え
            this.sys_control.isGamePlaying=true;
            game_start();
        });



       

        //中断ボタンが押されたとき
        this.elements.get("game-stop-button").addEventListener('click', (event) =>{
            this.gamePause();
        });

        



        //aiに手を聞くボタンが押されたとき
        this.elements.get("ask-ai-button").addEventListener('click', async(event) =>{

            const button = event.target;

            // ボタンを無効化
            button.disabled = true;

            const hold_lie = sys_control.add_lie;
            const hold_deep_num = sys_control.deep_num;

            this.sys_control.add_lie =1.0;
            this.sys_control.deep_num = 3;
            
            await cpuMove(true);

            this.sys_control.add_lie = hold_lie;
            this.sys_control.deep_num = hold_deep_num;


            // 処理終了後にボタンを有効化
            button.disabled = false;

        });

        //まったボタンが押された
        this.elements.get("game-previos-move-button").addEventListener('click', async(event) =>{
            //cpuが思考中でないなら有効
            if(!sys_control.cpuNowThinking){

                const mrcObj = this.sys_control.mainRecoardCenterProccess;
                const backKey =  mrcObj.mainData[mrcObj.nowUuid].previosUuid;
                let back2Key = null;
                if (backKey){//nullチェック
                    back2Key = mrcObj.mainData[backKey].previosUuid;
                }
                if (backKey && back2Key){//nullチェック
                    mrcObj.mainSelect(back2Key);//本譜select更新＆盤面変更
                }
            }
        });


        //cpuのカスタムを閉じるボタンが押されたとき
        this.elements.get("cpu-custom-close-button").addEventListener('click', (event) =>{

            //選択ボックスの内容を反映させる
            
            this.sys_control.deep_num = Number(this.elements.get("cpu-option-deep-num").value);
            this.sys_control.add_lie = Number(this.elements.get("cpu-option-add_lie").value)/10;

            //カスタム画面を隠す
            this.elements.get("cpu-level-custom-screen").classList.toggle('hidden'); // hiddenクラスを切り替え
            this.elements.get("hide-main-content").classList.toggle('hidden'); // hiddenクラスを切り替え
        });



        //CPUの強さを選択したとき
        this.elements.get("cpu-level-custom-select").addEventListener('change', (event) =>{

            const value = event.target.value;
            if (value == "cpulevelCustom"){
                //CPUカスタム画面を開く
                this.elements.get("cpu-level-custom-screen").classList.toggle('hidden'); // hiddenクラスを切り替え
                this.elements.get("hide-main-content").classList.toggle('hidden'); // hiddenクラスを切り替え
                this.elements.get("cpu-level-custom-screen").scrollIntoView({ behavior: 'smooth' });
                this.elements.get("cpu-level-custom-select").selectedIndex = -1;
            }else{
                sys_control.setCpuLevel(value);
            }
            


        });

        // 各要素にクリックイベントを設定

        /*
        this.cpuLevelSelectboxElements.forEach(element => {
            element.addEventListener('change', (event) => {
                const value = event.target.value;
                if (value == "cpulevelCustom"){
                    //CPUカスタム画面を開く
                    this.elements.get("cpu-level-custom-screen").classList.toggle('hidden'); // hiddenクラスを切り替え
                    this.elements.get("hide-main-content").classList.toggle('hidden'); // hiddenクラスを切り替え
                    this.elements.get("cpu-level-custom-screen").scrollIntoView({ behavior: 'smooth' });
                }else{
                    sys_control.setCpuLevel(value);
                }
            });
        });
        */
        


        //カスタム画面　CPUの読みの深さの選択がされたとき
        this.elements.get("cpu-option-deep-num").addEventListener('click', (event) =>{
            const selectedValue = event.target.value;
            sys_control.deep_num = Number(selectedValue);


        });

        //カスタム画面　cpuの読みのブレが選択されたとき
        this.elements.get("cpu-option-add_lie").addEventListener('click', (event) =>{
            const selectedValue = event.target.value;
            sys_control.add_lie = Number(selectedValue)/10;


        });



        //ファイルのセーブ用のテキスト生成ボタンが押されたとき
        this.elements.get("save-button").addEventListener('click', (event) =>{
            const saveText = sys_control.saveLoad.getSaveData();
            this.elements.get("file-textarea").value = saveText;

        });
        
        //ファイルのロードボタンが押されたとき
        this.elements.get("load-button").addEventListener('click', (event) =>{
            const jsonString = this.elements.get("file-textarea").value;
            this.sys_control.saveLoad.Load(jsonString);
            this.updateSelectElement();
        });


        //システムコントローラの変数にアクセスできるようにしておく
        this.sys_control = sys_control;
        
        //盤面上のこのマスを強調する
        this.strong_move_point=[];

        //最初に石の個数を初期化する
        this.updateCountStone(mainRecoardCenterProccess.game.getBlackStouneCount(),mainRecoardCenterProccess.game.getWhiteStouneCount());

        //手番の表示を更新
        this.update_now_turn_display(mainReversiGame.board.turn);
    }

    gamePause(){
        this.sys_control.isGamePlaying=false;
        this.toggleClassGameStart();//GUIの表示非表示切り替え

        //棋譜の描画を更新
        this.mainRecordSelectIndex = mainRecoardCenterProccess.mainData[mainRecoardCenterProccess.nowUuid].turn_num;
        this.updateSelectElement();//棋譜のセレクトボックスの更新s
    }

    toggleClass(){
        //検討に使うGUIと対戦中に使うGUIの表示非表示を切り替える
        //const element = document.getElementById('myElement');


        for(const key in this.elements.registerElements){
            this.elements.get(key).classList.toggle('hidden'); // hiddenクラスを切り替え
        }

    }

    toggleClassGameStart(){
        //検討に使うGUIと対戦中に使うGUIの表示非表示を切り替える
        //const element = document.getElementById('myElement');
        for(const key in this.elements.registerElements){
            if (this.elements.isGamePlayHideElement(key)){
                this.elements.get(key).classList.toggle('hidden'); // hiddenクラスを切り替え
            }
           
        }

    }
    updateSelectElement(){
        //本譜の表示を更新

        this.mainSelectElement.innerHTML = ''; // すべての項目を削除
        let key = this.sys_control.mainRecoardCenterProccess.startKey;
        while(true){
            const newOption = document.createElement('option'); // 新しいoption要素を作成
            newOption.text = this.sys_control.mainRecoardCenterProccess.mainData[key].name; // 表示テキスト
            newOption.value = key; // value属性
            newOption.className = "default-selectbox-design";
            this.mainSelectElement.add(newOption); // select要素に追加

            key = this.sys_control.mainRecoardCenterProccess.mainData[key].selectedBranchKey;
            if (!key){
                break;
            }

        }
        

        this.updateBranchSelectElement();
        this.mainSelectScrollValue();//本譜のセレクトボックスの選択位置を復旧
    }

    //本譜のセレクトボックスの選択位置を更新する
    mainSelectScrollValue(){
        if (this.mainRecordSelectIndex==-1){
            this.mainSelectElement.selectedIndex = this.mainSelectElement.options.length - 1;//一番下のデータに合わせてカーソルを移動させる
        }else{
            this.mainSelectElement.selectedIndex = this.mainRecordSelectIndex;
        }
    }


    updateBranchSelectElement(){
        //分岐の表示を更新

        const key = this.sys_control.mainRecoardCenterProccess.nowUuid;
        this.branchSelectElement.innerHTML = ''; // すべての項目を削除
        
        if (this.sys_control.mainRecoardCenterProccess.mainData[key].nextUuid.length==0){
            //表示するものが全くない場合は空白を挿入

            const newOption = document.createElement('option'); // 新しいoption要素を作成
            newOption.text = ""; // 表示テキスト
            newOption.value = "-1"; // value属性
            newOption.className = "default-selectbox-design";
            this.branchSelectElement.add(newOption); // select要素に追加

        }else{
            for(let i=0;i<this.sys_control.mainRecoardCenterProccess.mainData[key].nextUuid.length;i++){
                const k = this.sys_control.mainRecoardCenterProccess.mainData[key].nextUuid[i];//分岐データ１つ分。
                const newOption = document.createElement('option'); // 新しいoption要素を作成
                newOption.text = this.sys_control.mainRecoardCenterProccess.mainData[k].name; // 表示テキスト
                newOption.value = k; // value属性
                newOption.className = "default-selectbox-design";
                this.branchSelectElement.add(newOption); // select要素に追加
    
            }
        }


    }

    //石の個数の表示を更新する
    updateCountStone(black_count,white_count){
        const blackCountElement = document.getElementById('count-black-stone-text');
        const whiteCountElement = document.getElementById('count-white-stone-text');

        blackCountElement.textContent = ''+black_count;
        whiteCountElement.textContent = ''+white_count;


    }
    //今のターンの表示を更新
    update_now_turn_display(turn){
        const blackCountElement = document.getElementById('is-black-turn-display'); 
        const whiteCountElement = document.getElementById('is-white-turn-display');
        
        if (turn) {
            // 黒のターンの場合
            if (!blackCountElement.classList.contains('is-turn-display')) {
                blackCountElement.classList.add('is-turn-display'); // クラスを追加
            }
            if (whiteCountElement.classList.contains('is-turn-display')) {
                whiteCountElement.classList.remove('is-turn-display'); // クラスを削除
            }
        } else {
            // 白のターンの場合
            if (!whiteCountElement.classList.contains('is-turn-display')) {
                whiteCountElement.classList.add('is-turn-display'); // クラスを追加
            }
            if (blackCountElement.classList.contains('is-turn-display')) {
                blackCountElement.classList.remove('is-turn-display'); // クラスを削除
            }
        }
        




        blackCountElement.classList
    }
    

}