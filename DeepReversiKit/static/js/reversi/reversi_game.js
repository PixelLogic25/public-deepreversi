class ReversiGame {
    constructor(board) {
        //def __init__(self, board=None , none_possible_move = True,none_history = True) -> None:

        this.directions = [1, -1, 8, -8, 7, -7, 9, -9];
        this.turn_num = 0;
        this.possible_move = [];
        this.possible_move_array = Array(66).fill(false);//0~63:possibe move 64:pass 65:game end
        
        this.history = [];
        this.game_end = false;
        this.board = null;

        if (board){
           this.board = new ReversiBoard(board);
        }else{
            this.board = new ReversiBoard();
        }

        this.updatePossibleMoves();
    }

    //盤面を巻き戻したときであってもゲームを終了したかどうかを判定することができる
    //処理が重いので大量に呼び出さないこと
    isGameEnd(){
        let result = false;//この値をメソッドの結果として返す
        this.updatePossibleMoves();
        if (this.possible_move[0]==77){
            this.changeTurn();//手番交代
            this.updatePossibleMoves();//置ける場所更新

            if (this.possible_move[0]==77){
                result=true;
            }

            //一度手番を交代しているので戻す
            this.changeTurn();
            this.updatePossibleMoves();//置ける場所更新
        }
        return result;
    }

    flipStones(move) {
        let flipMask = toDesignatedSizeBigInt(0,64);

        for (let d of this.directions) {
            let mask = toDesignatedSizeBigInt(0,64);
            let n = move;

            while (true) {
                if ((d === -1 || d === 7 || d === -9) && n % 8 === 0) break;
                if ((d === 1 || d === -7 || d === 9) && n % 8 === 7) break;

                n += d;
                if (n < 0 || n >= 64) break; // 盤面外チェック
                //console.log("move:"+move+" n:"+n+" d:"+d);
                if (!(this.board.opponent_board & BigInt(1)<<BigInt(n))) break; // 相手の石ではない場合停止

                mask = mask | (BigInt(1) << BigInt(n));
            }

            // 自分の石に到達したかのチェック
            if (n >= 0 && n < 64 && (this.board.player_board & BigInt(1)<<BigInt(n))) {
                flipMask |= mask; // 相手の石をひっくり返す
            }
        }

        return flipMask;
    }

    possibleFlipStones(move) {
        for (let d of this.directions) {
            let n = move;
            let flag = false;

            while (true) {
                if ((d === -1 || d === 7 || d === -9) && n % 8 === 0) break;
                if ((d === 1 || d === -7 || d === 9) && n % 8 === 7) break;

                n += d;
                if (n < 0 || n >= 64) break; // 盤面外チェック
                if (!(this.board.opponent_board & BigInt(1)<<BigInt(n))) break; // 相手の石ではない場合停止

                flag = true;
            }

            // 自分の石に到達したかのチェック
            if (flag && n >= 0 && n < 64 && (this.board.player_board & BigInt(1)<<BigInt(n))) {
                return true;
            }
        }

        return false;
    }

    makeMove(move) {
        if (move > 63 && move!=77) {
            return 'Erorr';
        }
        
        this.game_end = false;
        if (move==77){
            this.changeTurn();
            this.updatePossibleMoves();
            this.turn_num++;

            if (this.possible_move[0] === 77) {
                this.game_end = true;
                return 'end';
            }


            //return '';
        }

        let flipMask = this.flipStones(move);

        if (flipMask) {
            this.board.player_board ^= (BigInt(1) << BigInt(move)) | flipMask;
            this.board.opponent_board ^= flipMask;

            this.changeTurn();
            this.updatePossibleMoves();

            this.turn_num++;

            if (this.possible_move[0] === 77) {
                return 'pass';
            }
        }

        return '';
    }

    changeTurn() {
        this.board.changeTurn();
    }

    updatePossibleMoves() {
        this.possible_move = [];
        this.possible_move_array = Array(66).fill(false);

        let tmp1 = getInversedBigIntBit(this.board.player_board | this.board.opponent_board,64)
        let tmp2 = (BigInt(1)<<BigInt(65))-BigInt(1);
        let emptyBoard = tmp1 & tmp2;


        for (let move = 0; move < 64; move++) {
            let tmp = BigInt(1)<<BigInt(move);
            if (emptyBoard & (BigInt(1)<<BigInt(move))) {
                if (this.possibleFlipStones(move)) {
                    this.possible_move.push(move);
                    this.possible_move_array[move] = true;
                }
            }
        }

        if (this.possible_move.length === 0) {
            this.possible_move = [77]; // パスを意味する
            this.possible_move_array[64]=true;
        }
    }

    getBoardIntArray64() {
        let boardArray = new Array(64).fill(0); // 64要素の配列を0で初期化

        for (let i = 0; i < 64; i++) {
            let playerBit = (this.board.player_board >> BigInt(i)) & BigInt(1); // i番目のビットが立っているか
            let opponentBit = (this.board.opponent_board >> BigInt(i)) & BigInt(1); // i番目のビットが立っているか

            if (this.board.turn) {
                // this.board.turn が true の場合
                if (playerBit) {
                    boardArray[i] = -1; // プレイヤーの石が置かれている場所は -1
                } else if (opponentBit) {
                    boardArray[i] = 1; // 相手の石が置かれている場所は 1
                }
            } else {
                // this.turn が false の場合
                if (playerBit) {
                    boardArray[i] = 1; // プレイヤーの石が置かれている場所は 1
                } else if (opponentBit) {
                    boardArray[i] = -1; // 相手の石が置かれている場所は -1
                }
            }
        }

        return boardArray;
    }

    getBlackStouneCount(){
        if (this.board.turn){
            return this.board.player_board.toString(2).split('0').join('').length;
        }else{
            return this.board.opponent_board.toString(2).split('0').join('').length;
        }

    }
    getWhiteStouneCount(){
        if (this.board.turn){
            return this.board.opponent_board.toString(2).split('0').join('').length;
        }else{
            return this.board.player_board.toString(2).split('0').join('').length;
        }

    }

}
