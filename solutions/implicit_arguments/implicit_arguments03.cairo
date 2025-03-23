// What is really neat with implicit arguments is that they are returned implicitly by any function using them
// This is a very powerful feature of the language since it helps with readability, letting the developer omit
// implicit arguments in the subsequent function calls.

// I AM NOT DONE

// TODO: implement the "black_box" function body to make the test pass

// Do not change the function signature!
func black_box{secret : felt}(){
    // Make the magic happen here :)
    let secret = 'very secret!';
    return();
}

// Do not change the test
func test__secret_change() -> felt{
    alloc_locals;
    local secret;
    %{
        ids.secret = program_input["secret"]
    %}
    with secret{
        black_box();
    }

    return secret;
}
