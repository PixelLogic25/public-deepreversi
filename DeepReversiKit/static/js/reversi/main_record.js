class MainRecordData{

    constructor(){
        this.move63 = [];//次の手の打った場所63形式（複数個）
        this.moveA1 = [];//次の手の打った場所A1形式（複数個）
        this.previosUuid = "";//前の手のUUID（１つで固定）
        this.nextUuid = [];//次の手のUUID（複数個）
        this.board = null;//盤面データ(64個の石情報、手番(黒か白か))
        this.name = "";//表示する名前
        this.previosMove = -1;//前の盤面から今の盤面になることになった、打たれた手

        this.selectedBranchKey = "";//直前に選択した分岐のkey

        this.branchRecordData = [];

        this.turn_num = 0;

    }
}



class MainBoardCenterProcess{
    constructor(game,mainBoard){
        this.numId=0;
        //const GAME_END_MAXIMAM_TURN_NUM = 65;

        this.mainData = {};
        
        //this.main_record_select_box_data = {};


        this.alphabet =[["A","B","C","D","E","F","G","H"],["a","b","c","d","e","f","g","h"]];
        this.nowUuid = this.GenerateUUID();
        this.startKey = this.nowUuid;

        this.mainData[this.nowUuid] = new MainRecordData();
        this.mainData[this.nowUuid].name = "初期盤面";
        this.mainData[this.nowUuid].board = new ReversiBoard();
        this.mainData[this.nowUuid].turn_num = 0;





        this.game = game;
        this.mainBoard = mainBoard;





    }

    mainSelect(key){
        if (key in this.mainData){
            this.nowUuid = key;

            this.game.board = new ReversiBoard(this.mainData[key].board);//ディープコピー
            this.game.updatePossibleMoves();//打てる場所を更新
            this.mainBoard.updateBoard([this.mainData[key].previosMove]);


        }else{

        }
    }

    branchSelect(key){
        if (key in this.mainData){
            this.mainData[this.nowUuid].selectedBranchKey=key;
            this.mainBoard.updateBoard([this.mainData[key].previosMove]);
        } 

    }

    add(move63){

        let game_result = "";
        //記録を追加しつつ、盤面も弄る。
        if (this.nowUuid in this.mainData){
            let nowData = this.mainData[this.nowUuid];
            
            const index = nowData.move63.indexOf(move63);
            if (index!=-1){
                //打った手はすでに過去に打たれている
                //①同じ手となるuuidを取得
                const uuid = nowData.nextUuid[index];

                //②nowBoardUuidに①で得たuuidを代入する。
                this.nowUuid = uuid;
                //③盤面(MainBoard)をMainRecordDataのキーnowBoardUuidで得られる盤面で更新

                this.game.board = new ReversiBoard(this.mainData[uuid].board);
                this.game.updatePossibleMoves();
                    
             }else{

                    //打った手から盤面を生成して一旦変数に保存。

                    //ユニークなuuidを生成（以下newUuid）
                    const newUuid = this.GenerateUUID();
                    
                    //MainRecordDataにnowBoardUuidをキーとした要素に以下のデータを追加の処理をする。
                    //「次の手の打った場所63形式」に①から得た打った手63形式
                    //「次の手の打った場所A1形式」に①から得た打った手A1形式
                    //「次の手のUUID」にnewUuid


                    this.mainData[this.nowUuid].move63.push(move63);//次の手の打った場所63形式（複数個）
                    this.mainData[this.nowUuid].moveA1.push(this.Convert63toA1(move63,this.game.board.turn));//次の手の打った場所A1形式（複数個）
                    this.mainData[this.nowUuid].nextUuid.push(newUuid);//次の手のUUID（複数個）
                    this.mainData[this.nowUuid].selectedBranchKey = newUuid;//分岐の一番上を選んでいるものとする。


                    //this.mainData[this.nowUuid].selectedBranchKey = newUuid;//本譜の表示を分岐後
                    
                
                    //MainRecordDataにnewUuidをキーとしたデータで更新する。
                    //nowBoardUuidにnewUuidを代入する。
                   
                    this.mainData[newUuid]= new MainRecordData();
                    this.mainData[newUuid].previosUuid = this.nowUuid;
                    game_result = this.game.makeMove(move63);//次の盤面を生成。
                    this.mainData[newUuid].board = new ReversiBoard(this.game.board);
                    this.mainData[newUuid].name = this.Convert63toA1(move63,this.game.board.turn);
                    this.mainData[newUuid].previosMove = move63;
                    this.mainData[newUuid].turn_num = this.mainData[this.nowUuid].turn_num+1;

                    this.nowUuid = newUuid;
             }
                

        }else{
            //ここに到達はありえないはず
        }
        //打った手のあと、パスしか手がないときはパスを打つ。その記録もする。
        if (game_result=="pass"){
            game_result=this.add(77);
        }else if(game_result=="end"){
            //ゲーム終了処理を書く。
        }
    }





    Convert63toA1(move63,turn){
        if (move63 < 0 || 63<move63 && move63!=77){
            return 'Error Convert63toA1:Move63は0～63,77です 受け取った値:'+move63
        }

        if (move63==77){
            return 'PASS'
        }
        const x = move63%8;
        const y = Math.floor(move63/8)+1;
        
        if (turn){
            return this.alphabet[0][x] + y;
        }else{
            return this.alphabet[1][x] + y;
        }

    }

    GenerateUUID(length = 15){
        let uuid = '';
        do{
            const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            const charactersLength = characters.length;
            uuid = '';
            
            for (let i = 0; i < length; i++) {
                const randomIndex = Math.floor(Math.random() * charactersLength);
                uuid += characters[randomIndex];
            }
        }while(uuid in this.mainData);
        
        return uuid;
        //this.numId++;
        //return ''+this.numId;
    }
    

    
}