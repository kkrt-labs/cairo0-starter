
// Function and other definitions can be scoped in namespaces, making the code more readable.

// I AM NOT DONE

// TODO: make the test pass!

// Do not change anything but the test
namespace my_namespace{
    func returns_something() -> felt{
        return 42;
    }
}

// Change the following test to make it pass
func test_hello(){
    let result = my_namespace.returns_something();
    assert result = 42;
    return();
}
