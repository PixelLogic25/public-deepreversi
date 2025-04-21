

function isElementAtIndex(array, index) {
    return array[index] !== undefined;
  }


function getInversedBigIntBit(bigint,length){
    let bitLength=0;
    if (length){
      bitLength=length;
    }else{
    // 全体のビット長を計算する (たとえば、debug4の長さを取得して反転対象にする)
      bitLength = bigint.toString(2).length;
    }


    // 指定のビット長で全ビットが1の値を作る (例: 111...111)
    let mask = (BigInt(1) << BigInt(bitLength)) - BigInt(1);

    // ビット反転を行う
    return ~bigint & mask;


}

//BigIntの長さを指定する。
function toDesignatedSizeBigInt(bigintValue,size){
  const maskBit = (BigInt(1) << BigInt(size)) - BigInt(1);  // sizeで指定した数の長さのビットマスク
  return BigInt(bigintValue) & maskBit;

}