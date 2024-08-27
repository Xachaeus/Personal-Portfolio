
var reg = {
  "00000" : 0,
  "00001" : 0,
  "00010" : 0,
  "00011" : 0,
  "00100" : 0,
  "00101" : 0,
  "00110" : 0,
  "00111" : 0,
  "01000" : 0,
  "01001" : 0,
  "01010" : 0,
  "01011" : 0,
  "01100" : 0,
  "01101" : 0,
  "01110" : 0,
  "01111" : 0,
  "10000" : 0,
  "10001" : 0,
  "10010" : 0,
  "10011" : 0,
  "10100" : 0,
  "10101" : 0,
  "10110" : 0,
  "10111" : 0,
  "11000" : 0,
  "11001" : 0,
  "11010" : 0,
  "11011" : 0,
  "11100" : 0,
  "11101" : 0,
  "11110" : 0,
  "11111" : 0,
};

var mem = new Uint8Array(0x10000); //Initialize memory

var BUS = extend(0); //Initialize 16-bit bus

var FL = "00001"; //ZF, LF, GT, CF, AF

var PC = "11101";
var LR = "11110";
var SP = "11100";
var ZR = "11111";
var AR = "11000";

var cc_names = {'eq':'000', 'ne':'001', 'lt':'010', 'le':'011',
                'gt':'100', 'ge':'101', 'cs':'110', 'al':'111'}

var limited_reg_names = {'a':'00', 'b':'01', 'c':'10', 'd':'11'}

var reg_names = {
  "x0":"00000", "x1":"00001", "x2":"00010", "x3":"00011",
  "x4":"00100", "x5":"00101", "x6":"00110", "x7":"00111",
  "x8":"01000", "x9":"01001", "x10":"01010", "x11":"01011",
  "x12":"01100", "x13":"01101", "x14":"01110", "x15":"01111",
  "x16":"10000", "x17":"10001", "x18":"10010", "x19":"10011",
  "x20":"10100", "x21":"10101", "x22":"10110", "x23":"10111",
  "x24":"11000", "x25":"11001", "x26":"11010", "x27":"11011",
  "x28":"11100", "x29":"11101", "x30":"11110", "x31":"11111",
  "a":"11000", "b":"11001", "c":"11010", "d":"11011",
  "pc":"11101", "lr":"11110", "sp":"11100", "zr":"11111"
}

function add_binary(a, b){
  var dec = Number(parseInt(a, 2)) + Number(parseInt(b, 2));
  return dec.toString(2);
}

function to_16_bits(num, len){
  return 0xffff&((num<<(32-len))>>(32-len));
}

function extend(num){
  return 0xffff&(((num<<16)>>16));
}

function get_neg(num){
  return (num<<16)>>16;
}

function get_5_bits(num){
  let s = ((0x1f&num) >>> 0).toString(2);
  return ("0".repeat(5-s.length) + s);
}

function get_8_bits(num){
  let s = ((0xff&num) >>> 0).toString(2);
  return ("0".repeat(8-s.length) + s);
}

function get_13_bits(num){
  let s = ((0x1fff&num) >>> 0).toString(2);
  return ("0".repeat(13-s.length) + s);
}

function get_16_bits(num){
  let s = ((0xffff&num) >>> 0).toString(2);
  return ("0".repeat(16-s.length) + s);
}


function set_flags(val, carry=false, overflow=false){
  let z = (extend(val)==0) ? "1" : "0";
  let l = ((0x8000&val)==1) ? "1" : "0";
  let v = (overflow) ? "1" : "0";
  let c = (val > 0xffff || carry) ? "1" : "0";
  let a = "1";
  FL = z+l+v+c+a;
}

function check_flags(F){
  switch (F){
    case "000":
      return FL[0]=="1";
    case "001":
      return FL[2]=="1";
    case "010":
      return FL[0]=="0" && FL[1]=="1";
    case "011":
      return FL[0]=="1" || FL[1]=="1";
    case "100":
      return FL[0]=="0" && FL[1]=="0";
    case "101":
      return FL[0]=="1" || FL[1]=="0";
    case "110":
      return FL[3]=="1";
    case "111":
      return FL[4]=="1";
  }
}

function load_memory(addr){
  return (mem[addr]<<8)+mem[addr+1];
}
function store_memory(addr, val){
  mem[addr+1] = 0xff&val; mem[addr] = val>>>8;
}
function load_bits(addr){
  let s = (0xffff&(((mem[addr]<<8)+mem[addr+1]) >>> 0)).toString(2);
  return ("0".repeat(16-s.length)) + s;
}
function store_bits(addr, bits){
  store_memory(addr, parseInt(bits, 2));
}

function execute_instruction(instr){
  if (instr.length != 16) {return 1;}
  switch (instr[0]){
    case "0": //3-bit instruction
      let Rd = instr.substring(3,8);
      let Im = parseInt(instr.substring(8), 2);
      let I = parseInt(instr.substring(3), 2);
      switch (instr.substring(1,3)){
        case "00": //PUT
          reg[Rd] = extend((reg[Rd]&0xff00) + (0xff&Im)); break;
        case "01": //ACC
          reg[AR] += extend(to_16_bits(I, 13)); break;
        case "10": //B
          reg[PC] = 0xffff&(reg[PC] + to_16_bits(I, 13));
          console.log(to_16_bits(I, 13));
          break;
        case "11": //BL
          reg[LR] = reg[PC] + 2; reg[PC] = extend(reg[PC] + extend(to_16_bits(I, 13))); break;
      }
      break;

    case "1": //6-bit instruction
      let Rn = instr.substring(6,11);
      let Rm = instr.substring(11);
      let F = instr.substring(13);
      let Rmf = add_binary(instr.substring(11,13), "11000");
      let N = instr.substring(11);
      let num=0;
      switch (instr.substring(1,6)){
          
        case "00000": //ASH
          num = parseInt(N.substring(1),2)+1;
          if (N[0]=="0") {reg[Rn] = extend(0xffff&(reg[Rn] << num));}
          else {reg[Rn] = extend(0xffff&(reg[Rn] >> num));}
          break;
          
        case "00001": //LSH
          num = parseInt(N.substring(1),2)+1;
          if (N[0]=="0") {reg[Rn] = extend(0xffff&(reg[Rn] << num));}
          else {reg[Rn] = extend(0xffff&(reg[Rn]) >>> num);}
          break;
          
        case "00010": //AND
          if (check_flags(F)){
            reg[Rn] = extend(reg[Rn] & reg[Rmf]);
          }
          break;
          
        case "00011": //NAND
          if (check_flags(F)){
            reg[Rn] = extend(~(reg[Rn] & reg[Rmf]));
          }
          break;
          
        case "00100": //NOT
          if (check_flags(F)){
            switch(instr.substring(11,2)){
              case "00":
                reg[Rn] = extend(~reg[Rn]);
                break;
              case "01":
                reg[Rn] = extend(-reg[Rn]);
                break;
            }
          }
          break;
          
        case "00101": //FST
          if(check_flags(F)){
            set_flags(reg[Rn]);
          }
          break;
          
        case "00110": //ORR
          if(check_flags(F)){
            reg[Rn] = extend(reg[Rn] | reg[Rmf]);
          }
          break;
          
        case "00111": //XOR
          if(check_flags(F)){
            reg[Rn] = extend(reg[Rn] ^ reg[Rmf]);
          }
          break;
          
        case "01000": //ADD
          if(check_flags(F)){
            reg[Rn] = extend((0xffff&reg[Rn]) + (0xffff&reg[Rmf]));
          }
          break;
          
        case "01001": //ADDS
          if(check_flags(F)){
            let res = (0xffff&reg[Rn]) + (0xffff&reg[Rmf])
            let carry = res > 0xffff;
            let overflow = ((0x8000&reg[Rn]) == (0x8000&reg[Rmf])) && ((0x8000&reg[Rn]) != (0x8000&res));
            reg[Rn] = extend(res);
            set_flags(res, carry, overflow);
          }
          break;
          
        case "01010": //SUB
          if(check_flags(F)){
            reg[Rn] = extend(reg[Rn] - reg[Rmf]);
          }
          break;
          
        case "01011": //SUBS
          if(check_flags(F)){
            let res = reg[Rn] - reg[Rmf];
            let carry = res < 0;
            let overflow = ((0x8000&reg[Rn]) == (0x8000&reg[Rmf])) && ((0x8000&reg[Rn]) != (0x8000&res));
            reg[Rn] = extend(res);
            set_flags(res, carry, overflow);
          }
          break;
          
        case "01100": //MUL
          if(check_flags(F)){
            reg[Rn] = extend(reg[Rn] * reg[Rmf]);
          }
          break;
          
        case "01101": //MULS
          if(check_flags(F)){
            let res = reg[Rn] * reg[Rmf];
            let carry = res > 0xffff;
            let overflow = ((0x8000&reg[Rn]) == (0x8000&reg[Rmf])) && ((0x8000&reg[Rn]) != (0x8000&res));
            reg[Rn] = extend(res);
            set_flags(res, carry, overflow);
          }
          break;
          
        case "01110": //UDIV
          if(check_flags(F)){
            let res = (reg[Rn] >>> 0) / (reg[Rmf] >>> 0);
            reg[Rn] = extend(res);
          }
          break;
          
        case "01111": //SDIV
          if(check_flags(F)){
            let res = (reg[Rn]) / (reg[Rmf]);
            reg[Rn] = extend(res);
          }
          break;
          
        case "10000": //BR (S)
          if(check_flags(F)){
            reg[PC] += reg[Rn];
          }
          break;
          
        case "10001": //BA
          if(check_flags(F)){
            reg[PC] = reg[Rn] - 2;
          }
          break;
          
        case "10010": //BLR
          if(check_flags(F)){
            reg[LR] = reg[PC] + 2;
            reg[PC] += reg[Rn];
          }
          break;
          
        case "10011": //BLA
          if(check_flags(F)){
            reg[LR] = reg[PC] + 2;
            reg[PC] = reg[Rn] - 2;
          }
          break;
          
        case "10100": //MVT
          if(check_flags(F)){
            reg[Rmf] = reg[Rn];
          }
          break;
          
        case "10101": //MVF
          if(check_flags(F)){
            reg[Rn] = reg[Rmf];
          }
          break;
          
        case "10110": //MOV
          reg[Rn] = reg[Rm];
          break;
          
        case "10111": //OUT (S)
          if(check_flags(F)){
            switch(instr.substring(11,13)){
              case "00":
                BUS = reg[Rn];
                break;
              case "01":
                reg[Rn] = BUS;
                break;
            }
          }
          break;
          
        case "11000": //PUSH (S)
          if(check_flags(F)){
            reg[SP] -= 2;
            reg[SP] = extend(reg[SP])>>>0;
            store_memory(reg[SP], reg[Rn]);
          }
          break;
          
        case "11001": //POP (S)
          if(check_flags(F)){
            reg[Rn] = load_memory(reg[SP]);
            reg[SP] += 2;
            reg[SP] = extend(reg[SP])>>>0;
          }
          break;
          
        case "11010": //STRC
          if(check_flags(F)){
            store_memory(reg[Rn], reg[Rmf]);
          }
          break;
          
        case "11011": //LDRC
          if(check_flags(F)){
            reg[Rmf] = load_memory(reg[Rn]);
          }
          break;
          
        case "11100": //STR
          store_memory(reg[Rn], reg[Rm]);
          break;
          
        case "11101": //LDR
          reg[Rm] = load_memory(reg[Rn]);
          break;
          
        case "11110": //STRO
          store_memory(extend(reg[Rn] + N), reg[AR]);
          break;
          
        case "11111": //LDRO
          reg[AR] = load_memory(extend(reg[Rn] + N));
          break;
      }
      break;
  }
  reg[PC] = 0xffff&(reg[PC] + 2);
  return 0;
}







function preprocess_assembly(){

  let os_code = `
//Set up branch table
PUT B, _end
PUSH B
PUT B, _start
PUSH B
PUT B, _brk
PUSH B
PUT B, _done
PUSH B
//Begin SVC loop
_svc:
MOV A, 0xfffe //Bottom of stack
MOV C, 1
ADD x0, C
MOV C, 2
MUL x0, C //Offset from bottom of stack
MOV C, x0
SUB A, C //Address of subroutine to branch to
LDR A, B
BA B //Go to subroutine

_brk: //Allocate heap memory. X1 is # of bytes
MOV A, 0xfffe
LDR A, B
MOV X0, B
MOV C, X1
ADD B, C
STR A, B
RET

_done:
MOV x0, 0xffff
OUT x0
b _done

`
  
  let doc = document.getElementById("editor");

  let text = os_code + doc.innerText + "\n_end:";
  
  let lines = text.split(/\r?\n/);
  const instructions = [];
  for (const line of lines){
    let code_line = line.split("//")[0]
    let new_items = code_line.split(';');
    for (let item of new_items){
      if (item != ""){
        item = item.replace(',', ' ').split(/\s/).filter(function(x) {return x.trim() != ''});
        instructions.push(item);
      }
    }
  }
  const expanded_instructions = [];
  for (const instr of instructions){
    if(instr[0].includes(':')){expanded_instructions.push(instr[0]); continue;}
    var instr_parts = instr[0].split('.');
    var base_instr = instr_parts[0].toUpperCase();
    let cc = 'al';
    if(instr_parts.length > 1){cc = instr_parts[1];}

    var Rn = null;
    var Rm = null;
    var I = null;
    var N = null;
    var Bn = null;
    var l = "";
    
    if(instr.length>1) {
      
      Rn = instr[1].toLowerCase();

      if(instr[1].substring(0,2) == "0x"){
        Bn = (0xffff&parseInt(instr[1],16))>>>0;
      }
      else if(instr[1].substring(0,2) == "0b"){
        Bn = (0xffff&parseInt(instr[1].substring(2),2))>>>0;
      }
      else{
        Bn = (0xffff&parseInt(instr[1],10))>>>0;
      }
      
    }
    if(instr.length>2) {
      
      Rm = instr[2].toLowerCase();

      if(instr[2].substring(0,2) == "0x"){
        I = (0xffff&parseInt(instr[2],16))>>>0;
      }
      else if(instr[2].substring(0,2) == "0b"){
        I = (0xffff&parseInt(instr[2].substring(2),2))>>>0;
      }
      else{
        I = (0xffff&parseInt(instr[2],10))>>>0;
      }

      if(instr[2].substring(0,2) == "0x"){
        N = (0x1f&parseInt(instr[2],16))>>>0;
      }
      else if(instr[2].substring(0,2) == "0b"){
        N = (0x1f&parseInt(instr[2].substring(2),2))>>>0;
      }
      else{
        N = (0x1f&parseInt(instr[2],10))>>>0;
      }
      
      l = instr[2];
      
    }

    //if(!(Rn in reg_names)){throw new Error("Unknown register alias!");}
    
    switch (base_instr){
      //
      //NEED TO FINISH ASSEMBLY EXPANSION!!!!
      //
      case "PUT":
        if (isNaN(parseInt(l))){
          expanded_instructions.push(["PUT", Rn, l]);
        }
        else if (I<256){
          expanded_instructions.push(["PUT", Rn, I]);
        }
        else{
          expanded_instructions.push(["PUT", Rn, 0xff&(I>>>8)]);
          expanded_instructions.push(["LSH", Rn, 8]);
          expanded_instructions.push(["PUT", Rn, 0xff&I]);
        }
        break;

      case "ACC":
        expanded_instructions.push(["ACC", I])

      case "MOV":
        if(cc=="al" && isNaN(parseInt(l))){
          expanded_instructions.push(["MOV", Rn, Rm]);
        }
        else if(cc=="al"){
          if (isNaN(parseInt(l))){
            expanded_instructions.push(["PUT", Rn, l]);
          }
          else{
            expanded_instructions.push(["PUT", Rn, 0xff&(I>>>8)]);
            expanded_instructions.push(["LSH", Rn, 8]);
            expanded_instructions.push(["PUT", Rn, 0xff&I]);
          }
          
        }
        else if(Rn in limited_reg_names){
          expanded_instructions.push(["MVT", Rm, Rn, cc]);
        }
        else if(Rm in limited_reg_names){
          expanded_instructions.push(["MVF", Rn, Rm, cc]);
        }
        else{
          throw new Error("Cannot use conditional move without at least one limited register!")
        }
      break;

      case "IN":
        expanded_instructions.push(["OUT", Rn, "b", cc]);
        break;

      case "OUT":
        expanded_instructions.push(["OUT", Rn, "a", cc]);
        break;

      case "STR":
        if(cc=="al" && !isNaN(parseInt(l))){
          expanded_instructions.push(["STRO", Rn, N]);
        }
        else if(cc=="al"){
          expanded_instructions.push(["STR", Rn, Rm]);
        }
        else if(Rm in limited_reg_names){
          expanded_instructions.push(["STRC", Rn, Rm, cc]);
        }
        else{
          throw new Error("Improper syntax for STR instruction!");
        }
        break;

      case "STRO":
        expanded_instruction.push(["STRO", Rn, N]);
        break;

      case "LDR":
        if(cc=="al" && !isNaN(parseInt(l))){
          expanded_instructions.push(["LDRO", Rn, N]);
        }
        else if(cc=="al"){
          expanded_instructions.push(["LDR", Rn, Rm]);
        }
        else if(Rm in limited_reg_names){
          expanded_instructions.push(["LDRC", Rn, Rm, cc]);
        }
        else{
          throw new Error("Improper syntax for LDR instruction!");
        }
        break;

      case "LDRO":
        expanded_instructions.push(["LDRO", Rn, N]);

      case "PUSH":
        expanded_instructions.push(["PUSH", Rn, 'a', cc]);
        break;

      case "POP":
        expanded_instructions.push(["POP", Rn, 'a', cc]);
        break;

      case "B":
        if(Rn in reg_names){
          expanded_instructions.push(["BA", Rn, "a", cc]);
        }
        else if(isNaN(parseInt(Rn))){
          expanded_instructions.push(["B", Rn]);
        }
        else{
          expanded_instructions.push(["B", Bn]);
        }
        break;

      case "BL":
        if(Rn in reg_names){
          expanded_instructions.push(["BLA", Rn, "a", cc]);
        }
        else if(isNaN(parseInt(Rn))){
          expanded_instructions.push(["BL", Rn]);
        }
        else{
          expanded_instructions.push(["BL", Bn]);
        }
        break;

      case "BR":
        expanded_instructions.push(["BR", Rn, 'a', cc]);
        break;

      case "BA":
        expanded_instructions.push(["BA", Rn, 'a', cc]);
        break;

      case "BLR":
        expanded_instructions.push(["BLR", Rn, 'a', cc]);
        break;

      case "BLA":
        expanded_instructions.push(["BLA", Rn, 'a', cc]);
        break;

      case "LSL":
        expanded_instructions.push(["LSH", Rn, N]);
        break;

      case "LSR":
        expanded_instructions.push(["LSH", Rn, -N]);
        break;

      case "ASR":
        expanded_instructions.push(["ASH", Rn, -N]);
        break;

      case "LSH":
        expanded_instructions.push(["LSH", Rn, N]);
        break;

      case "ASH":
        expanded_instructions.push(["ASH", Rn, N]);
        break;

      case "NOT":
        expanded_instructions.push(["NOT", Rn, 'a', cc]);
        break;

      case "NEG":
        expanded_instructions.push(["NOT", Rn, 'b', cc]);
        break;

      case "FST":
        expanded_instructions.push(["FST", Rn, 'a', cc]);
        break;

      case "CALL":
        expanded_instructions.push(["BL", Rn]);
        break;

      case "RET":
        expanded_instructions.push(["BA", "lr", 'a', cc]);
        break;

      case "SVC":
        expanded_instructions.push(["BL", "_svc"]);
        break;

      default:
        expanded_instructions.push([base_instr, Rn, Rm, cc]);
    }
  }
  doc = document.getElementById("preprocess-out");
  doc.innerText = JSON.stringify(expanded_instructions);
  return expanded_instructions;
}




function resolve_assembly(){
  let instructions = JSON.parse(document.getElementById("preprocess-out").innerText);
  const labels = {};
  let new_instrs = [];
  //Find lables and record positions
  for (let i=0; i<instructions.length; i++){
    if(typeof instructions[i] === 'string' || instructions[i] instanceof String){
      labels[instructions[i].replace(':','')] = (i-Object.keys(labels).length)*2;
    }
    else{
      new_instrs.push(instructions[i]);
    }
  }
  //Replace mentions of labels with positions
  for (let j=0; j<new_instrs.length; j++){
    //Labels used with branch instructions are replaced with relative jump
    if(new_instrs[j][1] in labels){
      new_instrs[j][1] = (labels[new_instrs[j][1]]-j*2) - 2;
    }
    //Labels used with immediate instructions are replaced with absolute address
    if(new_instrs[j][2] in labels){
      let Ln = labels[new_instrs[j][2]];
      if(Ln < 256){
        new_instrs[j][2] = Ln;
      }
      else{
        let Ln0 = (0xff00&Ln)>>>8;
        let Ln1 = 0xff&Ln;
        new_instrs.splice(j, 1, ["PUT", new_instrs[j][1], Ln0],
                                ["LSH", new_instrs[j][1], 8],
                                ["PUT", new_instrs[j][1], Ln1]);
      }
    }
  }
  
  document.getElementById("preprocess-out").innerText = JSON.stringify(new_instrs);
}



function translate_assembly(){
  let instructions = JSON.parse(document.getElementById("preprocess-out").innerText)
  let output_bits = [];
  
  for (instr of instructions){

    let Rn = null; let Rm = null; let cc = null; let N = 0;

    if (instr.length>1){Rn = instr[1];}
    if (instr.length>2){Rm = instr[2];}
    if (instr.length>3){cc = instr[3];}
    
    switch (instr[0]){

      case "PUT":
        output_bits.push("000" + reg_names[Rn] + get_8_bits(Rm));
        break;

      case "ACC":
        output_bits.push("001" + get_13_bits(parseInt(Rn)));
        break;

      case "B":
        output_bits.push("010" + get_13_bits(parseInt(Rn)));
        break;

      case "BL":
        output_bits.push("011" + get_13_bits(parseInt(Rn)));
        break;

      case "ASH":
        Rm = Number(Rm);
        if(Rm<0){N = 0x10 | ((0xf&Math.abs(Rm))-1);}
        else{N = ((0xf&Math.abs(Rm))-1);}
        output_bits.push("100000" + reg_names[Rn] + get_5_bits(N));
        break;

      case "LSH":
        Rm = Number(Rm);
        if(Rm<0){N = 0x10 | ((0xf&Math.abs(Rm))-1);}
        else{N = ((0xf&Math.abs(Rm))-1);}
        output_bits.push("100001" + reg_names[Rn] + get_5_bits(N));
        break;

      case "AND":
        output_bits.push("100010" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "NAND":
        output_bits.push("100011" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "NOT":
        output_bits.push("100100" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "FST":
        output_bits.push("100101" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "ORR":
        output_bits.push("100110" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "XOR":
        output_bits.push("100111" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "ADD":
        output_bits.push("101000" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "ADDS":
        output_bits.push("101001" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "SUB":
        output_bits.push("101010" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "SUBS":
        output_bits.push("101011" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "MUL":
        output_bits.push("101100" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "MULS":
        output_bits.push("101101" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "UDIV":
        output_bits.push("101110" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "SDIV":
        output_bits.push("101111" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "BR":
        output_bits.push("110000" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "BA":
        output_bits.push("110001" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "BLR":
        output_bits.push("110010" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "BLA":
        output_bits.push("110011" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "MVT":
        output_bits.push("110100" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "MVF":
        output_bits.push("110101" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "MOV":
        output_bits.push("110110" + reg_names[Rn] + reg_names[Rm]);
        break;

      case "OUT":
        output_bits.push("110111" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "PUSH":
        output_bits.push("111000" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "POP":
        output_bits.push("111001" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "STRC":
        output_bits.push("111010" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "LDRC":
        output_bits.push("111011" + reg_names[Rn] + limited_reg_names[Rm] + cc_names[cc]);
        break;

      case "STR":
        output_bits.push("111100" + reg_names[Rn] + reg_names[Rm]);
        break;

      case "LDR":
        output_bits.push("111101" + reg_names[Rn] + reg_names[Rm]);
        break;

      case "STRO":
        N = Number(Rm);
        output_bits.push("111110" + reg_names[Rn] + get_5_bits(N));
        break;

      case "LDRO":
        N = Number(Rm);
        output_bits.push("111111" + reg_names[Rn] + get_5_bits(N));
        break;

      
      default:
        throw new Error("Invalid assembly!");
    }
  }

  document.getElementById("binary-out").innerText = output_bits.join("\n");
}

/*
execute_instruction("0001100111111111"); //PUT B, 255
execute_instruction("1000001100100111"); //LSH B, 8
execute_instruction("0001100111111111"); //PUT B, 255
execute_instruction("0001100000000011"); //PUT A, 3
//execute_instruction("0001100100000000"); //PUT B, 0
//execute_instruction("1101101100100000"); //MOV B, X0
execute_instruction("1010011100001111"); //ADDS A, B
*/
//store_bits(0, "0001100100000010"); //PUT B, 2
//store_bits(2, "1000001100100111"); //LSH B, 8
//store_bits(4, "0001100111111111"); //PUT B, 255
//store_bits(2, "0001100000000011"); //PUT A, 3
//store_bits(4, "1010011100001111"); //ADDS A, B
//store_bits(6, "1101111100000111");

function parse_program(){

  let doc = document.getElementById("binary-out");
  let text = doc.innerText;
  let lines = text.split(/\r?\n/);
  let addr = 0;
  for (const line of lines){
    store_bits(addr, line);
    addr += 2;
  }
  reset_program();
  show_registers();
}

function reset_program(){
  for (const key in reg){
    reg[key] = 0;
  }
  FL = "00001";
  let lines = JSON.parse(document.getElementById("preprocess-out").innerText);
  document.getElementById("instr-display").innerText = JSON.stringify(lines[0]);
}

function show_registers(){
  let reg_output = "";
  for(let i = 0; i<32; i++){
    reg_output += "X" + i + ": " + get_neg(reg[get_5_bits(i)]) + "\n";
  }
  reg_output += "Flags: " + FL + "\n";
  reg_output += "Bus: " + BUS + "\n";
  document.getElementById("reg-display").innerText = reg_output;
}

function do_next_step(){
  instr = load_bits(reg[PC]);
  execute_instruction(instr);
  reg[ZR] = 0;
  show_registers();
  let lines = JSON.parse(document.getElementById("preprocess-out").innerText);
  document.getElementById("instr-display").innerText = JSON.stringify(lines[reg[PC]/2]);
}

function run_program(){
  while (BUS != 0xffff){
    do_next_step();
  }
}
//console.log(reg)
//console.log(mem.slice(256, 300))
//console.log(FL)