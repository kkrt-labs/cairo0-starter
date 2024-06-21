// Cairo hints can be useful for delegating heavy computation.
// This pattern is at the very heart of Cairo: verification is much faster than computation.
// However, as hints are not part of the final Cairo bytecode, a malicious program may provide wrong results.
// You should always verify computations done inside hints.

// I AM NOT DONE

// TODO: Compute the result of "x modulo n" inside a hint using python's `divmod`
// Don't forget to make sure the result is correct.

func modulo() -> felt{
    alloc_locals;
    local x;
    local n;
    %{
        ids.x = program_input["x"]
        ids.n = program_input["n"]
    %}

    local quotient;
    local remainder;
    %{
        # TODO: Compute the quotient and remainder inside the hint
        #print(ids.quotient)
        #print(ids.remainder)
    %}

    %{
        q, r = divmod(ids.x, ids.n)
        ids.quotient = q
        ids.remainder = r
    %}
    assert x = quotient * n + remainder;
    // TODO: verify the result is correct

    return remainder;
}
