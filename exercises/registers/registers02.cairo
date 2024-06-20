
// I AM NOT DONE

// Cairo memory is immutable.
// Once a memory cell has been assigned, its value CANNOT be changed.
// The program will crash if someone tries to assign a new, different, value to an already initialized memory cell.
// However, trying to assign a memory cell twice, or more, **with the same value** won't cause any harm.
// This property can be used to assert the value of a cell.

// TODO
// Rewrite this function in a high level syntax, using tempvar and assert
func crash(){
    // [ap] = 42; ap++
    // [ap - 1] = 42
    // [ap - 1] = 21

    tempvar value = 42;
    assert value = 42;
    assert value = 21;
    return();
}

// TODO
// Rewrite this funtion in a low level syntax
func assert_42(number : felt){
    // assert number = 42;

    assert [fp-3] = 42;
    return();
}

// TODO
// Write this function body so:
// if the memory cell pointed by `p_number` is not initialized, set it to 42
// else, if the value is initialized and different from 42, crash
// else, do nothing and return
func assert_pointer_42(p_number : felt*){
    assert [p_number] = 42;
    return();
}

// TODO
// Write this function body so:
// if the memory cell pointed by `p_number` is set to 42, do nothing and return
// else crash
func assert_pointer_42_no_set(p_number : felt*){
    assert 42 = [p_number];
    return();
}

// TESTS

from starkware.cairo.common.alloc import alloc

func test_crash(){
    %{ expect_revert() %}
    crash();

    return();
}

func test_assert_42(){
    alloc_locals;
    local number;
    %{
        ids.number = program_input["number"]
    %}
    assert_42(number);
    return();
}

func test_assert_pointer_42_initialized(){
    let (mem_zone : felt*) = alloc();
    assert mem_zone[0] = 42;
    assert mem_zone[1] = 21;
    assert_pointer_42(mem_zone);
    return();
}

func test_assert_pointer_42_initialized_ko(){
    let (mem_zone : felt*) = alloc();
    assert mem_zone[0] = 42;
    assert mem_zone[1] = 21;
    assert_pointer_42(mem_zone + 1);
    return();
}

func test_assert_pointer_42_not_initialized_ok(){
    let (mem_zone : felt*) = alloc();
    assert mem_zone[0] = 42;
    assert_pointer_42(mem_zone);

    assert_pointer_42(mem_zone + 1);
    assert mem_zone[1] = 42;
    return();
}

func test_assert_pointer_42_not_initialized_revert(){
    let (mem_zone : felt*) = alloc();
    assert mem_zone[0] = 42;
    assert_pointer_42(mem_zone);

    assert_pointer_42(mem_zone + 1);
    assert mem_zone[1] = 21;

    return();
}

func test_assert_pointer_42_no_set(){
    let (mem_zone : felt*) = alloc();
    assert mem_zone[0] = 42;
    assert mem_zone[1] = 21;

    assert_pointer_42_no_set(mem_zone);

    return();
}

func test_assert_pointer_42_no_set_ko(){
    let (mem_zone : felt*) = alloc();
    assert mem_zone[0] = 42;
    assert mem_zone[1] = 21;

    assert_pointer_42_no_set(mem_zone);
    assert_pointer_42_no_set(mem_zone + 1);

    return();
}

func test_assert_pointer_42_no_set_crash(){
    let (mem_zone : felt*) = alloc();

    assert_pointer_42_no_set(mem_zone);

    return();
}
