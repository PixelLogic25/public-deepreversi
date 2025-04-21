
class ReversiSendReceive{
    constructor(sys_control){
        this.lastBranchData = [];
        this.sys_control=sys_control;
    }
    //必ず4byte(32bit)のサイズで、BigIntをByteに変換する。
    bigintToBytes(bigint) {
        let hex = bigint.toString(16); // BigIntを16進数文字列に変換
        let zeroUme='';
        for( let i=0;i<(8-hex.length) ; i++){
            zeroUme+='0';
            
        }
        hex = zeroUme + hex; // 長さが4byteになるように、先頭に0を付ける
        const bytes = new Uint8Array(hex.length / 2);
        for (let i = 0; i < hex.length; i += 2) {
            bytes[i / 2] = parseInt(hex.substr(i, 2), 16); // 2桁ずつ16進数をバイトに変換
        }
        return bytes;
    }

    bigIntSplitBySize(bigInt){
        
    }

    bigIntArrayToBytes(bigIntArray) {



        // 各BigIntをバイト配列に変換
        const byteArrays = bigIntArray.map(this.bigintToBytes);
        
        // 全てのバイト配列の長さを合計
        const totalLength = byteArrays.reduce((acc, arr) => acc + arr.length, 0);
        
        // 一つのArrayBufferに全てのバイトを格納
        const result = new Uint8Array(totalLength);
        let offset = 0;
        for (const byteArray of byteArrays) {
            result.set(byteArray, offset);
            offset += byteArray.length;
        }
        return result;
    }
    getSendAskCpuData(rg,deep_num){

        if (deep_num<1){
            return null;//発生してほしくない
        }
        this.lastBranchData = [];

        //console.log(rg.possible_move);

       
        if (1<deep_num){
            //２手以上深読みする場合
            for (let i=0;i<rg.possible_move.length;i++){

                const move = rg.possible_move[i];
                let tmp_rg = new ReversiGame(new ReversiBoard(rg.board));//今の盤面をディープコピー
                let tmp_before_rg = new ReversiGame(new ReversiBoard(rg.board));//今の盤面をディープコピーして、こちらは手を打たず盤面を更新しない。
                let pass_check = tmp_rg.makeMove(move);

                //if (pass_check=='pass'){
                    //tmp_rg.changeTurn();
                //}


                this.lastBranchData = this.lastBranchData.concat(this.getBranch(tmp_rg,deep_num-1,[i],tmp_before_rg));
            }
        }else{
            let possible_max = 0;
            const possible_list = [];
            //1手読みのとき
            for (let i=0;i<rg.possible_move.length;i++){
                const move = rg.possible_move[i];
                const tmp_rg = new ReversiGame(new ReversiBoard(rg.board));
                const tmp_before_rg = new ReversiGame(new ReversiBoard(rg.board));
                const pass_check = tmp_rg.makeMove(move);
                


                this.lastBranchData = this.lastBranchData.concat(this.getLastBranchData(tmp_rg,[i],tmp_before_rg));
                
                //着手可能数の計算の準備をする
                possible_list.push(tmp_rg.possible_move.length);
                if (possible_max<tmp_rg.possible_move.length){
                    possible_max = tmp_rg.possible_move.length;
                }
            }
            //着手可能数の計算をする
            for (let i=0;i<rg.possible_move.length;i++){
                this.lastBranchData[i].possible_per_1000x1000 = Math.floor(1000*1000*possible_list[i]/possible_max);
            }

        }
        return this.lastBranchData;
    }
    
    getBranch(rg,deep,branch_num_list,before_game){
        if (deep==0 || rg.game_end){
            
            return this.getLastBranchData(rg,branch_num_list,before_game);
        }
        let res = [];

        const tmp_possible_num_list = [];
        let last_count=0;
        let tmp_max_possible_num=0;
        //console.log(rg.possible_move);
        for (let i=0;i<rg.possible_move.length;i++){
            const move = rg.possible_move[i];
            const tmp_rg = new ReversiGame(new ReversiBoard(rg.board));//盤面のディープコピー
            
            tmp_rg.makeMove(move);//一手打った盤面を作る

            //最大着手可能数を計算するため着手可能数を一時保存
            if(deep==1 || tmp_rg.game_end){
                last_count++;
                tmp_possible_num_list.push(tmp_rg.possible_move.length);//着手可能数を代入していく
                if (tmp_max_possible_num<tmp_rg.possible_move.length){
                    tmp_max_possible_num = tmp_rg.possible_move.length;//最大着手可能数更新
                }
            }

            //concatは遅いので要改善
            res = res.concat(this.getBranch(tmp_rg,deep-1,branch_num_list.concat([i]),new ReversiGame(new ReversiBoard(rg.board))));

            
        }
        for(let i=0;i<last_count;i++){

            let tmp = (1000*1000*tmp_possible_num_list[i])/tmp_max_possible_num;
            tmp = Math.floor(tmp);
            res[res.length-last_count+i].possible_per_1000x1000 = tmp;

        }

        return res;
    }

    getLastBranchData(rg,branch_num_list,before_game){
        const tmp_lbd = new LastBranchData();
        tmp_lbd.before_board = new ReversiBoard(before_game.board);
        tmp_lbd.board = new ReversiBoard(rg.board);

        if (rg.board.turn == before_game.board.turn){
            tmp_lbd.is_continue_turn = 1;
        }else{
            tmp_lbd.is_continue_turn = 0;
        }
        
        //tmp_lbd.possible_num = before_game.possible_move.length;
        tmp_lbd.set_group_number(branch_num_list); //所属分岐末端番号(5手読みならサイズは5?　末端ほど後ろに格納)
        tmp_lbd.eval_num = 0.0;
        return tmp_lbd;
    }
    


    async sendAskCpu(rg,deep_num){
    
        //let deep_num=1;
        let sendData =[];
        let splitSendData=[];
        let sendDataByte=[];
        let rowSendData;
        
        sendData = this.getSendAskCpuData(rg,deep_num);
        const isError = [false];
        
        //送信するデータだけをBitInt型で抜き出す
        for(let i=0;i<sendData.length;i++){

            sendData[i].compile_board();//64bitのボードbitを32bitに分割する

            //手が打たれる前の盤面を、32bitサイズに分割された状態で代入
            Array.prototype.push.apply(splitSendData,sendData[i].get_bit_before_board(sendData[i].before_board.turn))
            //現在の盤面を、32bitサイズに分割された状態で代入
            Array.prototype.push.apply(splitSendData,sendData[i].get_bit_board(sendData[i].board.turn));
        
            
            //現在の手番を代入
            if (sendData[i].before_board.turn){
                splitSendData.push(toDesignatedSizeBigInt(BigInt(0),8));
            }else{
                splitSendData.push(toDesignatedSizeBigInt(BigInt(1),8));
            }

            //一手前の手番と今の手番が同じなら1、違うなら-1

            splitSendData.push(toDesignatedSizeBigInt(BigInt(sendData[i].is_continue_turn),8));
            
            splitSendData.push(toDesignatedSizeBigInt(sendData[i].possible_per_1000x1000,32));
           
        }
        //byte型へ変換
        rowSendData = this.bigIntArrayToBytes(splitSendData);

        //gzip形式で通信のデータを圧縮
        const compressedBytes = pako.gzip(rowSendData);

        let best_move = -1;
        //データをサーバーへ送信して結果を受信する。
        //サーバーからのデータが反映されたsendDataが渡される
        await this.sendDataToServer(compressedBytes, sendData , isError);
        if (isError[0]){
            //なにかしらエラー発生
            best_move =-1
        }else{
            //読みのブレを反映させる。
            this.AddLie(sendData);

            //求めやすいように形を変形
            const minimax = new Minimax();
            for(let i=0;i<sendData.length;i++){
                minimax.set_data(sendData[i].group_number,sendData[i].eval_num);
            }
            //minmax法で最善手を求める
            minimax.get_best_start(rg.board.turn);
            best_move = rg.possible_move[minimax.get_best()];
        }

        return best_move;
        
    }

    async sendDataToServer(compressedBytes, sendData , isError){
        await fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/octet-stream',
                'Content-Encoding': 'gzip',
                'Accept-Encoding': 'gzip'  // gzipデータを受け入れる指定
            },
            body: compressedBytes // 圧縮データを送信
        })
        .then(response => response.json())
        .then(data => {
            isError[0] = data["error"];
            for (let i=0 ;i<sendData.length;i++){
                sendData[i].eval_num = data["evals"][i];
            }
        })
        .catch(error => {
            isError[0] = true;
            console.error('Error:', error);
        });
    }


    AddLie(sendData){
        


        //評価値の中で最大値と最小値を調べる
        
        let max = -99999999;
        let min = 99999999;

        for(let i=0;i<sendData.length;i++){
            if (sendData[i].eval_num< min){
                min = sendData[i].eval_num;
            }
            if (max < sendData[i].eval_num){
                max = sendData[i].eval_num;
            }
        }

    
        const maxMinLength = max - min;
        const multi = this.sys_control.add_lie/100.0 * maxMinLength;

        for(let i=0;i<sendData.length;i++){
            sendData[i].eval_num += Math.random() * (multi*2) - multi;
        }
    }
}
