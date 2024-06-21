// Felts supports basic math operations.
// Only accepted operators (const excluded) are: +, -, * and /

// I AM NOT DONE

// TODO
// Return the solution of (x² + x - 2) / (x - 2)
func poly() -> felt{
    alloc_locals;
    local x;
    %{
        ids.x = program_input["x"];
    %}
    // FILL ME
    let res = (x * x + x - 2) / (x - 2);
    return res;  // Do not change
}
