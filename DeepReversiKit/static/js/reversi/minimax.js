class MinimaxData{
    constructor(){
        this.group = [];
        this.my_eval = 0;
    }
}

class Minimax{
    constructor(){
        this.data = [];
        this.max_deep = 0;
        this.is_multi_minus = [] ;
        this.ai_turn = null;
    }

    set_data(group,eval_num){
        const substitute_data = new MinimaxData();
        substitute_data.group = group.concat();
        substitute_data.my_eval = eval_num;
        this.data.push(substitute_data);
    }

    get_best_start(ai_turn){
        for(let i=0;i<this.data.length;i++){
            if (this.max_deep<this.data[i].group.length){
                this.max_deep = this.data[i].group.length;
            }
        }
        

        //末端がfalse、末端の一つ上のノードがtrue,その上がfalse...となるような配列を用意。
        this.is_multi_minus = [] ;

        let tmp_turn = false;


        if (this.max_deep%2==0){
            tmp_turn = false;
        }else{
            tmp_turn = false;
        }


        for(let i=this.max_deep-1;0<=i;i--){
            this.is_multi_minus[i]=tmp_turn;
            tmp_turn = !tmp_turn;
        }
        this.ai_turn = ai_turn;
    }

    get_best(){
        let res = 0;
        for(let deep = this.max_deep-1 ;0<=deep;deep--){

            let count=0;

            while(true){
                if (this.data.length<=count){
                    break;
                }
                let trigger=-1;
                let target = [];
                //let exit_flag = false;
                //末端で同じ親をもつノードをgroupを参考にして評価値同士を抜き出す
                while(true){
                    if (this.data.length<=count){
                        break;
                    }

                    //探索したい同じ深さのとき
                    if (this.data[count].group.length==deep+1){
                        
                        const last_group = this.data[count].group[deep];//グループ内で何番目かを取得
                        if (last_group == trigger+1){//前の取得した番号+1なら同じグループ
                            target.push(this.data.splice(count,1)[0]);
                            trigger = last_group;
                            continue;
                        }else{
                            //違うグループに突入したので計算処理へ
                            //exit_flag = true;
                            break;
                        }
                    }else{
                        if (!target.length==0){
                            //すでに抜き出したあとで、違う深さのデータを見つけたら計算処理へ
                            //exit_flag = true;
                            break;
                        }
                    }
                    count++;
                }

                //計算するデータが存在しているなら計算をする
                if (target.length!=0){
                    //マイナスをかける深さであるときは-1を掛け算する、そうでなければ ×1
                    
                    
                    for (let i = 0;i<target.length;i++){
                        //console.log(target[i].my_eval);
                        target[i].my_eval = target[i].my_eval * (this.is_multi_minus[deep] ? -1 : 1 );
                        //console.log(target[i].my_eval);
                    }
                    
                    
                    //最大値と最大値となる要素インデックスを取得。
                    let max = target[0].my_eval;
                    res=0;

                    for (let i = 1; i < target.length; i++) {
                        if (target[i].my_eval > max) {
                            max = target[i].my_eval;
                            res = i;
                        }
                    }

                    //グループの末端から一つ上の階層に行ってもらうため、末端の要素を削除したグループを作成
                    const group = [].concat(target[0].group.slice(0, -1));
                    //最大値となった要素を新しく追加する
                    this.set_data(group,target[res].my_eval*(this.is_multi_minus[deep] ? -1 : 1 ));
                }else{
                    //計算データがないので次の階層に行く。
                    break;
                }

            }

           
        }
        return res;
    }


}