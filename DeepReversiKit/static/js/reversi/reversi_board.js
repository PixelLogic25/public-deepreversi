class ReversiBoard {
    constructor(reversiBoard) {

        if (reversiBoard){
            this.player_board = reversiBoard.player_board
            this.opponent_board = reversiBoard.opponent_board
            this.turn = reversiBoard.turn;
        }else{
            this.player_board = toDesignatedSizeBigInt(0x0000000810000000,64);  //プレイヤーの初期配置
            this.opponent_board = toDesignatedSizeBigInt(0x0000001008000000,64);  //相手の初期配置
            this.turn = true;
            
        }
        //self.update_possible_moves()
        
        //self.history = History()
        //self.history.add(self)
    
        //self.turn_num=0
    }

    changeTurn(){
        [this.player_board, this.opponent_board] = [this.opponent_board, this.player_board];
        this.turn = !this.turn;
    }
   

}