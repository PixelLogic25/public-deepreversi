

//盤面の末端の情報をまとめたクラス。
class LastBranchData{
    constructor(){
        this.board = null;
        this.before_board= null;

        this.split_bit_board = [];

        
        this.is_continue_turn = 0 ;
        //this.possible_num = 0;//着手可能数（一手で打てる場所の数）
        //this.possible_max = 0;//一手での着手可能数の最大値

        this.possible_per_1000x1000=0;//着手可能数÷最大着手可能数の結果を１００万倍した値を入れる
        this.group_number =  []; //所属分岐末端番号(5手読みならサイズは5?　末端ほど後ろに格納)
        this.eval_num = 0.0;

        this.str_group_number = "";
    }

    //group_numberを代入するときに使う
    set_group_number(group_array){
        this.group_number = group_array;

        let str = ""
        group_array.forEach(element => {
            str += ""+element+"_";
        }); 

        this.str_group_number=str;
    }

    compile_board(){
        this.split_bit_board.push(this.get_split_bit_board(this.before_board.player_board,true));
        this.split_bit_board.push(this.get_split_bit_board(this.before_board.player_board,false));

        this.split_bit_board.push(this.get_split_bit_board(this.before_board.opponent_board,true));
        this.split_bit_board.push(this.get_split_bit_board(this.before_board.opponent_board,false));

        this.split_bit_board.push(this.get_split_bit_board(this.board.player_board,true));
        this.split_bit_board.push(this.get_split_bit_board(this.board.player_board,false));

        this.split_bit_board.push(this.get_split_bit_board(this.board.opponent_board,true));
        this.split_bit_board.push(this.get_split_bit_board(this.board.opponent_board,false));
    }

    get_bit_before_board(black_is_player){

        //return [this.split_bit_board[0],this.split_bit_board[1],this.split_bit_board[2],this.split_bit_board[3]];
        if (black_is_player){
            return [this.split_bit_board[0],this.split_bit_board[1],this.split_bit_board[2],this.split_bit_board[3]];
        }else{
            return [this.split_bit_board[2],this.split_bit_board[3],this.split_bit_board[0],this.split_bit_board[1]];
        }
        
        //return [this.split_bit_board[0],this.split_bit_board[1],this.split_bit_board[2],this.split_bit_board[3]];
    }

    get_bit_board(black_is_player){
        
        if (black_is_player){
            return [this.split_bit_board[4],this.split_bit_board[5],this.split_bit_board[6],this.split_bit_board[7]];
        }else{
            return [this.split_bit_board[6],this.split_bit_board[7],this.split_bit_board[4],this.split_bit_board[5]];
        }
            
       // return [this.split_bit_board[4],this.split_bit_board[5],this.split_bit_board[6],this.split_bit_board[7]];
    }
    get_split_bit_board(bit_board,isFrist){
        //bit_boardは64bitのbigintで来ることを前提にした関数
        //32bitの2つに分割
        if (isFrist){

            return toDesignatedSizeBigInt(bit_board>>BigInt(32),32)
        }else{
            //後ろ32bitのbitだけ取り出す
            const mask = BigInt(0xFFFFFFFF);

            return toDesignatedSizeBigInt(bit_board & mask,32)
        }

    }

}