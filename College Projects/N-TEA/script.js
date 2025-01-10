//Create data structures for emulator to use


var reg = { //Dictionary for accessing 32 registers from their binary names
  "00000" : 0, "00001" : 0, "00010" : 0, "00011" : 0,
  "00100" : 0, "00101" : 0, "00110" : 0, "00111" : 0,
  "01000" : 0, "01001" : 0, "01010" : 0, "01011" : 0,
  "01100" : 0, "01101" : 0, "01110" : 0, "01111" : 0,
  "10000" : 0, "10001" : 0, "10010" : 0, "10011" : 0,
  "10100" : 0, "10101" : 0, "10110" : 0, "10111" : 0,
  "11000" : 0, "11001" : 0, "11010" : 0, "11011" : 0,
  "11100" : 0, "11101" : 0, "11110" : 0, "11111" : 0,
};

var mem = new Uint8Array(0x10000); //Initialize memory

var BUS = 0; //Initialize 32-bit bus

var FL = "00001"; //ZF, LF, OF, CF, AF






//Define common values for ease of programming

var PC = "11101";
var LR = "11110";
var SP = "11100";
var ZR = "11111";
var AR = "11000";

//Define dictionaries for easy translation between common references and their bianry counterparts

var cc_names = {'eq':'000', 'ov':'001', 'lt':'010', 'le':'011',
                'gt':'100', 'ge':'101', 'cs':'110', 'al':'111',
                'co':'001', 'ci':'110'}

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

var bin_to_reg = {
  "00000":"X0", "00001":"X1", "00010":"X2", "00011":"X3",
  "00100":"X4", "00101":"X5", "00110":"X6", "00111":"X7",
  "01000":"X8", "01001":"X9", "01010":"X10", "01011":"X11",
  "01100":"X12", "01101":"X13", "01110":"X14", "01111":"X15",
  "10000":"X16", "10001":"X17", "10010":"X18", "10011":"X19",
  "10100":"X20", "10101":"X21", "10110":"X22", "10111":"X23",
  "11000":"X24", "11001":"X25", "11010":"X26", "11011":"X27",
  "11100":"X28", "11101":"X29", "11110":"X30", "11111":"X31",
}

var bin_to_special_reg = {
  "00":"A", "01":"B", "10":"C", "11":"D"
}

var bin_to_cc = {
  "000":"eq", "001":"ov", "010":"lt", "011":"le",
  "100":"gt", "101":"ge", "110":"cs", "111":"al"
}


//Utility functions
function add_binary(a, b){ //Add two binary strings
  var dec = Number(parseInt(a, 2)) + Number(parseInt(b, 2));
  return dec.toString(2);
}

function to_16_bits(num, len){ //Get number of any length in 16 bits assuming 2's complement
  return 0xffff&((num<<(32-len))>>(32-len));
}

function extend(num){ //Is this even necessary?
  return 0xffff&(((num<<16)>>16));
}

function get_neg(num){ //Does this serve any purpose?
  return (num<<16)>>16;
}

function get_5_bits(num){ //Get number as string with 5 bits
  let s = ((0x1f&num) >>> 0).toString(2);
  return ("0".repeat(5-s.length) + s);
}

function get_8_bits(num){ //Get number as string with 8 bits
  let s = ((0xff&num) >>> 0).toString(2);
  return ("0".repeat(8-s.length) + s);
}

function get_13_bits(num){ //Get number as string with 13 bits
  let s = ((0x1fff&num) >>> 0).toString(2);
  return ("0".repeat(13-s.length) + s);
}

function get_16_bits(num){ //Get number as string with 16 bits
  let s = ((0xffff&num) >>> 0).toString(2);
  return ("0".repeat(16-s.length) + s);
}

//Update flag register
function set_flags(val, carry=false, overflow=false){
  let z = (extend(val)==0) ? "1" : "0";
  let l = ((0x8000&val)==1) ? "1" : "0";
  let v = (overflow) ? "1" : "0";
  let c = (val > 0xffff || carry) ? "1" : "0";
  let a = "1";
  FL = z+l+v+c+a;
}

//Return whether binary-specified condition exists in flag register
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


//Interact with memory
function load_memory(addr){
  return (mem[addr]<<8)+mem[addr+1];
}
function store_memory(addr, val){
  mem[addr+1] = 0xff&val; mem[addr] = val>>>8;
}
function load_byte(addr){
  return mem[addr];
}
function store_byte(addr, val){
  mem[addr] = val;
}
function load_bits(addr){//Get string representation of memory
  let s = (0xffff&(((mem[addr]<<8)+mem[addr+1]) >>> 0)).toString(2);
  return ("0".repeat(16-s.length)) + s;
}
function store_bits(addr, bits){//Store string representation into memory
  store_memory(addr, parseInt(bits, 2));
}




//
//
//Interpreter function (for emulator)
//
//
function execute_instruction(instr){
  if (instr.length != 16) {return 1;}
  //Handle two primary formats
  switch (instr[0]){



    case "0": //3-bit instruction
      //Define common references
      let Rd = instr.substring(3,8);
      let Im = parseInt(instr.substring(8), 2);
      let I = parseInt(instr.substring(3), 2);
      switch (instr.substring(1,3)){
        case "00": //PUTL (M)
          reg[Rd] = extend((reg[Rd]&0xff00) + (0xff&Im)); break;
        case "01": //PUTH (M)
          reg[Rd] = extend((reg[Rd]&0x00ff) + (0xff00&(Im<<8))); break;
        case "10": //B (I)
          reg[PC] = 0xffff&(reg[PC] + to_16_bits(I<<1, 14));
          console.log(to_16_bits(I<<1, 14));
          break;
        case "11": //BL (I)
          reg[LR] = reg[PC] + 2; reg[PC] = extend(reg[PC] + extend(to_16_bits(I<<1, 14))); break;
      }
      break;



    case "1": //6-bit instruction
      //Define common references
      let Rn = instr.substring(6,11);
      let Rm = instr.substring(11);
      let F = instr.substring(13);
      let Rmf = add_binary(instr.substring(11,13), "11000");
      let N = instr.substring(11);
      let num=0;
      switch (instr.substring(1,6)){
          
        case "00000": //ASH (N)
          num = parseInt(N.substring(1),2)+1;
          if (N[0]=="0") {reg[Rn] = extend(0xffff&(reg[Rn] << num));}
          else {reg[Rn] = extend(0xffff&(reg[Rn] >> num));}
          break;
          
        case "00001": //LSH (N)
          num = parseInt(N.substring(1),2)+1;
          if (N[0]=="0") {reg[Rn] = extend(0xffff&(reg[Rn] << num));}
          else {reg[Rn] = extend(0xffff&(reg[Rn]) >>> num);}
          break;
          
        case "00010": //AND (F)
          if (check_flags(F)){
            reg[Rn] = extend(reg[Rn] & reg[Rmf]);
          }
          break;
          
        case "00011": //NAND (F)
          if (check_flags(F)){
            reg[Rn] = extend(~(reg[Rn] & reg[Rmf]));
          }
          break;
          
        case "00100": //NOT (S)
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
          
        case "00101": //FST (S)
          if(check_flags(F)){
            set_flags(reg[Rn]);
          }
          break;
          
        case "00110": //ORR (F)
          if(check_flags(F)){
            reg[Rn] = extend(reg[Rn] | reg[Rmf]);
          }
          break;
          
        case "00111": //XOR (F)
          if(check_flags(F)){
            reg[Rn] = extend(reg[Rn] ^ reg[Rmf]);
          }
          break;
          
        case "01000": //ADD (F)
          if(check_flags(F)){
            reg[Rn] = extend((0xffff&reg[Rn]) + (0xffff&reg[Rmf]));
          }
          break;
          
        case "01001": //ADDS (F)
          if(check_flags(F)){
            let res = (0xffff&reg[Rn]) + (0xffff&reg[Rmf])
            let carry = res > 0xffff;
            let overflow = ((0x8000&reg[Rn]) == (0x8000&reg[Rmf])) && ((0x8000&reg[Rn]) != (0x8000&res));
            reg[Rn] = extend(res);
            set_flags(res, carry, overflow);
          }
          break;
          
        case "01010": //SUB (F)
          if(check_flags(F)){
            reg[Rn] = 0xffff&(reg[Rn] - reg[Rmf]);
          }
          break;
          
        case "01011": //SUBS (F)
          if(check_flags(F)){
            let res = reg[Rn] - reg[Rmf];
            let carry = res < 0;
            let overflow = ((0x8000&reg[Rn]) == (0x8000&reg[Rmf])) && ((0x8000&reg[Rn]) != (0x8000&res));
            reg[Rn] = extend(res);
            set_flags(res, carry, overflow);
          }
          break;
          
        case "01100": //MUL (F)
          if(check_flags(F)){
            reg[Rn] = extend(reg[Rn] * reg[Rmf]);
          }
          break;
          
        case "01101": //MULS (F)
          if(check_flags(F)){
            let res = reg[Rn] * reg[Rmf];
            let carry = res > 0xffff;
            let overflow = ((0x8000&reg[Rn]) == (0x8000&reg[Rmf])) && ((0x8000&reg[Rn]) != (0x8000&res));
            reg[Rn] = extend(res);
            set_flags(res, carry, overflow);
          }
          break;
          
        case "01110": //UDIV (F)
          if(check_flags(F)){
            let res = (reg[Rn] >>> 0) / (reg[Rmf] >>> 0);
            reg[Rn] = extend(res);
          }
          break;
          
        case "01111": //SDIV (F)
          if(check_flags(F)){
            let res = (reg[Rn]) / (reg[Rmf]);
            reg[Rn] = extend(res);
          }
          break;
          
        case "10000": //BR and BLR (S)
          if(check_flags(F)){
            switch(instr.substring(11,13)){
              case "00":
                reg[PC] = reg[Rn] - 2;
                break;
              case "01":
                reg[LR] = reg[PC] + 2;
                reg[PC] = reg[Rn] - 2;
                break;
            }
          }
          break;
          
        case "10001": //SWAP (D)
          let temp = load_memory(reg[Rn]);
          store_memory(reg[Rn], reg[Rm]);
          reg[Rm] = 0xffff&temp;
          break;
          
        case "10010": //STRB (D)
          store_byte(reg[Rn], reg[Rmf]);
          break;
          
        case "10011": //LDRB (D)
          reg[Rm] = load_byte(reg[Rn]);
          break;
          
        case "10100": //MVT (F)
          if(check_flags(F)){
            reg[Rmf] = reg[Rn];
          }
          break;
          
        case "10101": //MVF (F)
          if(check_flags(F)){
            reg[Rn] = reg[Rmf];
          }
          break;
          
        case "10110": //MOV (D)
          reg[Rn] = reg[Rm];
          break;
          
        case "10111": //OUT (S)
          if(check_flags(F)){
            switch(instr.substring(11,13)){
              case "00": //Lo Write
                BUS = (0xffff0000&BUS) + reg[Rn];
                break;
              case "01": //Hi Write
                BUS = (0x0000ffff&BUS) + (reg[Rn]<<16);
                break;
              case "10": //Lo Read
                reg[Rn] = 0x0000ffff&BUS;
                break;
              case "11": //Hi Read
                reg[Rn] = (0xffff0000&BUS)>>>16;
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
          
        case "11010": //STRC (F)
          if(check_flags(F)){
            store_memory(reg[Rn], reg[Rmf]);
          }
          break;
          
        case "11011": //LDRC (F)
          if(check_flags(F)){
            reg[Rmf] = load_memory(reg[Rn]);
          }
          break;
          
        case "11100": //STR (D)
          store_memory(reg[Rn], reg[Rm]);
          break;
          
        case "11101": //LDR (D)
          reg[Rm] = load_memory(reg[Rn]);
          break;
          
        case "11110": //STRO (N)
          store_memory(extend(reg[Rn] + N), reg[AR]);
          break;
          
        case "11111": //LDRO (N)
          reg[AR] = load_memory(extend(reg[Rn] + N));
          break;
      }
      break;
  }
  reg[PC] = 0xffff&(reg[PC] + 2);
  return 0;
}


//
//
// STEEP Assembler Preprocessor
//
//
function preprocess_assembly(){
//Define assembly for the operating system
  let os_code = `
//Set up branch table
MOV B, _end
PUSH B
MOV B, _start
PUSH B
MOV B, _brk
PUSH B
MOV B, _done
PUSH B

//Begin SVC loop
_svc:
MOV A, 0xfffe //Bottom of stack
MOV C, 1
ADD x7, C
MOV C, 2
MUL x7, C //Offset from bottom of stack
MOV C, x7
SUB A, C //Address of subroutine to branch to
LDR A, B
BR B //Go to subroutine

_brk:
MOV A, 0xfffe
LDR A, B
MOV D, B
MOV C, X0
ADD B, C
STR A, B
MOV X0, D
RET

_done:
MOV x24, 0xffff
OUTL x24
OUTH x24
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

    //Define common references

    var Rn = null;
    var Rm = null;
    var I = null;
    var N = null;
    var Bn = null;
    var l = "";
    
    if(instr.length>1) {
      
      Rn = instr[1].toLowerCase();

      if(instr[1].substring(0,2) == "0x"){
        Bn = (0xffff&parseInt(instr[1],16))>>>1;
      }
      else if(instr[1].substring(0,2) == "0b"){
        Bn = (0xffff&parseInt(instr[1].substring(2),2))>>>1;
      }
      else{
        Bn = (0xffff&parseInt(instr[1],10))>>>1;
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
    
    switch (base_instr){ //Expand each instruction to directly-translatable instructions
      //
      //NEED TO FINISH ASSEMBLY EXPANSION!!!!
      //
      case "PUTL":
        expanded_instructions.push(["PUTL", Rn, 0xff&I]);
        break;

      case "PUTH":
        expanded_instructions.push(["PUTH", Rn, 0xff&I]);
        break;

      case "MOV":
        if(cc=="al" && l in reg_names){ //Regular MOV
          expanded_instructions.push(["MOV", Rn, Rm]);
        }
        else if(cc=="al"){ //Non-conditionals
          if (isNaN(parseInt(l))){ //MOV with label
            expanded_instructions.push(["PUTL", Rn, l]);
          }
          else{ //MOV with constant
            expanded_instructions.push(["PUTH", Rn, 0xff&(I>>>8)]);
            expanded_instructions.push(["PUTL", Rn, 0xff&I]);
          }
          
        }
        else if(Rn in limited_reg_names){ //Should be MVT
          expanded_instructions.push(["MVT", Rm, Rn, cc]);
        }
        else if(Rm in limited_reg_names){ //Should be MVF
          expanded_instructions.push(["MVF", Rn, Rm, cc]);
        }
        else{ //Wrong form
          throw new Error("Cannot use conditional move without at least one limited register!")
        }
      break;

      case "INL":
        expanded_instructions.push(["OUT", Rn, "c", cc]);
        break;

      case "INH":
        expanded_instructions.push(["OUT", Rn, "d", cc]);
        break;

      case "OUTL":
        expanded_instructions.push(["OUT", Rn, "a", cc]);
        break;

      case "OUTH":
        expanded_instructions.push(["OUT", Rn, "b", cc]);
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
        break;

      case "PUSH":
        expanded_instructions.push(["PUSH", Rn, 'a', cc]);
        break;

      case "POP":
        expanded_instructions.push(["POP", Rn, 'a', cc]);
        break;

      case "B":
        if(Rn in reg_names){ //Should be BR
          expanded_instructions.push(["BR", Rn, "a", cc]);
        }
        else if(isNaN(parseInt(Rn))){ //Branch with label
          expanded_instructions.push(["B", Rn]);
        }
        else{ //Branch with constant
          expanded_instructions.push(["B", Bn]);
        }
        break;

      case "BL":
        if(Rn in reg_names){ //Should be BLR
          expanded_instructions.push(["BR", Rn, "b", cc]);
        }
        else if(isNaN(parseInt(Rn))){ //Branch with label
          expanded_instructions.push(["BL", Rn]);
        }
        else{ //Branch with constant
          expanded_instructions.push(["BL", Bn]);
        }
        break;

      case "BR":
        expanded_instructions.push(["BR", Rn, 'a', cc]);
        break;

      case "BLR":
        expanded_instructions.push(["BR", Rn, 'b', cc]);
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
        expanded_instructions.push(["BR", "lr", 'a', cc]);
        break;

      case "SVC":
        expanded_instructions.push(["BL", "_svc"]);
        break;

      case "PAUSE":
        expanded_instructions.push(["PUTL", "x27", 255]);
        expanded_instructions.push(["PUTH", "x27", 255]);
        expanded_instructions.push(["OUT", "x27", 'a', cc]);
        expanded_instructions.push(["OUT", "x27", 'b', cc]);
        expanded_instructions.push(["PUTL", "x27", 0]);
        expanded_instructions.push(["PUTH", "x27", 0]);
        expanded_instructions.push(["OUT", "x27", 'a', cc]);
        expanded_instructions.push(["OUT", "x27", 'b', cc]);

      default: //If no expansion given, treat the instruction as raw
        expanded_instructions.push([base_instr, Rn, Rm, cc]);
    }
  }
  doc = document.getElementById("preprocess-out");
  doc.innerText = JSON.stringify(expanded_instructions);
  return expanded_instructions;
}



//
//
// STEEP Assembler Reference Resolution (Linking)
//
//
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
      new_instrs[j][1] = (0xffff&((labels[new_instrs[j][1]]-j*2) - 2)) >> 1;
    }
    //Labels used with immediate instructions are replaced with absolute address
    if(new_instrs[j][2] in labels){
      let Ln = labels[new_instrs[j][2]];
      if(Ln < 256){
        new_instrs[j][2] = Ln;
      }
      else{ //Put address of label in register
        let Ln0 = (0xff00&Ln)>>>8;
        let Ln1 = 0xff&Ln;
        new_instrs.splice(j, 1, ["PUTH", new_instrs[j][1], Ln0],
                                ["PUTL", new_instrs[j][1], Ln1]);
      }
    }
  }
  
  document.getElementById("preprocess-out").innerText = JSON.stringify(new_instrs);
}



//
//
// STEEP Assembler Direct Translation (Assembly)
//
//
function translate_assembly(){
  let instructions = JSON.parse(document.getElementById("preprocess-out").innerText)
  let output_bits = [];
  
  for (instr of instructions){

    let Rn = null; let Rm = null; let cc = null; let N = 0;

    if (instr.length>1){Rn = instr[1];}
    if (instr.length>2){Rm = instr[2];}
    if (instr.length>3){cc = instr[3];}
    
    switch (instr[0]){

      case "PUTL":
        output_bits.push("000" + reg_names[Rn] + get_8_bits(Rm));
        break;

      case "PUTH":
        output_bits.push("001" + reg_names[Rn] + get_8_bits(Rm));
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

      case "SWAP":
        output_bits.push("110001" + reg_names[Rn] + reg_names[Rm]);
        break;

      case "STRB":
        output_bits.push("110010" + reg_names[Rn] + reg_names[Rm]);
        break;

      case "LDRB":
        output_bits.push("110011" + reg_names[Rn] + reg_names[Rm]);
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



//
//
// UX Functions for using emulator and assembler
//
//
function parse_program(){ //Load existing binary into program memory, starting at 0x0000

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
  console.log("Loaded " + lines.length*2 + " bytes of instructions!");
}




function reset_program(){ //Reset emulator to initial conditions
  for (const key in reg){
    reg[key] = 0;
  }
  FL = "00001";
  BUS = 0;
  let lines = JSON.parse(document.getElementById("preprocess-out").innerText);
  //Set instruction display
  //document.getElementById("instr-display").innerText = JSON.stringify(lines[0]);
  document.getElementById("instr-display").innerText = decode_binary_to_assembly(load_bits(0));
}



function show_registers(){ //Display registers in text form
  let reg_output = "";
  for(let i = 0; i<32; i++){
    let reg_val = reg[get_5_bits(i)];
    reg_output += ("X" + i + ": " + get_neg(reg_val) + " ".repeat(5) + get_16_bits(reg_val) + "\n");
  }
  reg_output += "Flags: " + FL + "\n";
  reg_output += "Bus: " + BUS + "\n";
  document.getElementById("reg-display").innerText = reg_output;
}


function decode_binary_to_assembly(instr){ //Turn binary instructions back into raw assembly

  let R = instr.substring(3,8);
  let Rn = instr.substring(6,11);
  let N = parseInt(instr.substring(11), 2);
  let Im = parseInt(instr.substring(8), 2);
  let Ib = parseInt(instr.substring(3), 2)<<1;
  let Rm = instr.substring(11);
  let Rmf = instr.substring(11,13);
  let cc = instr.substring(13);


  let eR = bin_to_reg[R];
  let eRn = bin_to_reg[Rn];
  let eRm = bin_to_reg[Rm];
  let ecc = bin_to_cc[cc];
  let eRmf = bin_to_special_reg[Rmf];
  
  switch (instr[0]){
    case "0":
      switch (instr.substring(1,3)){
        case "00":
          return `PUTL ${eR}, ${Im}`;
          break;
        case "01":
          return `PUTH ${eR}, ${Im}`;
          break;
        case "10":
          return `B ${Ib}`;
          break;
        case "11":
          return `BL ${Ib}`;
          break;
      }
      break;
    case "1":
      switch (instr.substring(1,6)){
        case "00000":
          return `ASH ${eRn}, ${N}`;
        case "00001":
          return `LSH ${eRn}, ${N}`;
        case "00010":
          return `AND.${ecc} ${eRn}, ${eRmf}`;
        case "00011":
          return `NAND.${ecc} ${eRn}, ${eRmf}`;
        case "00100":
          return `NOT.${ecc} ${eRn}, ${eRmf}`;
        case "00101":
          return `FST.${ecc} ${eRn}`;
        case "00110":
          return `ORR.${ecc} ${eRn}, ${eRmf}`;
        case "00111":
          return `XOR.${ecc} ${eRn}, ${eRmf}`;
        case "01000":
          return `ADD.${ecc} ${eRn}, ${eRmf}`;
        case "01001":
          return `ADDS.${ecc} ${eRn}, ${eRmf}`;
        case "01010":
          return `SUB.${ecc} ${eRn}, ${eRmf}`;
        case "01011":
          return `SUBS.${ecc} ${eRn}, ${eRmf}`;
        case "01100":
          return `MUL.${ecc} ${eRn}, ${eRmf}`;
        case "01101":
          return `MULS.${ecc} ${eRn}, ${eRmf}`;
        case "01110":
          return `UDIV.${ecc} ${eRn}, ${eRmf}`;
        case "01111":
          return `SDIV.${ecc} ${eRn}, ${eRmf}`;
        case "10000":
          return `BR.${ecc} ${eRn}`;
        case "10001":
          return `SWAP ${eRn}, ${eRm}`;
        case "10010":
          return `STRB ${eRn}, ${eRm}`;
        case "10011":
          return `LDRB ${eRn}, ${eRm}`;
        case "10100":
          return `MVT.${ecc} ${eRn}, ${eRmf}`;
        case "10101":
          return `MVF.${ecc} ${eRn}, ${eRmf}`;
        case "10110":
          return `MOV ${eRn}, ${eRm}`;
        case "10111":
          return `OUT.${ecc} ${eRn}, ${eRmf}`;
        case "11000":
          return `PUSH.${ecc} ${eRn}`;
        case "11001":
          return `POP.${ecc} ${eRn}`;
        case "11010":
          return `STRC.${ecc} ${eRn}, ${eRmf}`;
        case "11011":
          return `LDRC.${ecc} ${eRn}, ${eRmf}`;
        case "11100":
          return `STR ${eRn}, ${eRm}`;
        case "11101":
          return `LDR ${eRn}, ${eRm}`;
        case "11110":
          return `STRO ${eRn}, ${N}`;
        case "11111":
          return `LDRO ${eRn}, ${N}`;
      }
      break;
  }
  return "Error parsing binary!";
}



function do_next_step(){ //Set up emulator to execute the instruction referenced by PC
  let instr = load_bits(reg[PC]);
  execute_instruction(instr);
  reg[ZR] = 0;
  show_registers();
  let lines = JSON.parse(document.getElementById("preprocess-out").innerText);
  //Show next instruction in display
  //document.getElementById("instr-display").innerText = JSON.stringify(lines[reg[PC]/2]);
  document.getElementById("instr-display").innerText = decode_binary_to_assembly(load_bits(reg[PC]));
}



function run_program(){ //Continuously execute next step of program until BUS is -1
  while (BUS != -1){
    do_next_step();
  }
}

function load_assembly(){ 
  document.getElementById("fileInput").click();
  console.log(document.getElementById("fileInput"));
}



function quick_run(){ //Automatically perform full assembler cycle and run program until BUS is -1
  preprocess_assembly();
  resolve_assembly();
  translate_assembly();
  parse_program();
  run_program();
}

/*Example magnitude program

sqrt: //X0: Num
mov a, 2
mov c, 0
mov b, 0xffff
mov d, 1
mov x1, top
top:
add b, a //add b, 2
add c, d //add c, 1
subs x0, b
b.gt x1 //b.gt top
mov x0, c
ret

magnitude: //X0: Num1, X1: Num2
push lr
mov a, x0
mov b, x1
mul a, a
mul b, b
add a, b
mov x0, a //Sum of squares in x0
call sqrt
pop lr
ret

_start:
mov x0, 3
mov x1, 4
call magnitude

mov x7, 2
svc

*/