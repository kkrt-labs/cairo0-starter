// Getting pointer as function arguments let us modify the values at the memory address of the pointer;
// ...or not! Cairo memory is immutable. Therefore you cannot just update a memory cell.

// I AM NOT DONE

// TODO: Update the square function – you can change the body and the signature –
// to make it achieve the desired result: returning an array
// with the squared values of the input array.

from starkware.cairo.common.alloc import alloc

func square(array_len : felt, array : felt*){
    if (array_len == 0){
        return();
    }

    let squared_item = array[0] * array[0];
    assert [array] = squared_item;

    return square(array_len - 1, array + 1);
}

// You can update the test if the function signature changes.
func test__square() -> felt* {
    alloc_locals;
    local array_len;
    let (array) = alloc();

    %{
        ids.array_len = len(program_input["array"])
        segments.write_arg(ids.array, program_input["array"])
    %}
    let (new_array) = alloc();
    square(array_len, array);

    return new_array;
}
