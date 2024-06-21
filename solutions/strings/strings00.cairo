// Cairo supports short strings which are encoded as ASCII under the hood
// The felt is the decimal representation of the string in hexadecimal ASCII
// e.g. let hello_string = 'Hello';
//      let hello_felt = 310939249775;
//      let hello_hex = 0x48656c6c6f;
// https://www.cairo-lang.org/docs/how_cairo_works/consts.html#short-string-literals

// I AM NOT DONE

// TODO: Fix the say_hello function by returning the appropriate short strings
// Tip: Install the Starknet Converter Raycast extension to convert between felt and ASCII

func say_hello() -> (hello_string : felt, hello_felt : felt, hello_hex : felt){
    // FILL ME
    let hello_string = 'Hello Starklings';
    let hello_felt = '#L2-2022 #L3-2023';
    let hello_hex = 'buidl buidl buidl';
    return (hello_string, hello_felt, hello_hex);
}

// Do not change the test
func test_say_hello(){
    let (user_string, user_felt, user_hex) = say_hello();
    assert user_string = 'Hello Starklings';
    assert user_felt = 12011164701440182822452181791570417168947;
    assert user_hex = 0x627569646c20627569646c20627569646c;
    return();
}
