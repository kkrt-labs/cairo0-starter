

// Felts are integers defined in the range [0 ; P[, all compuations are done modulo P.
// Exercice resources: https://docs.cairo-lang.org/cairozero/hello_cairo/intro.html#the-primitive-type-field-element-felt

// I AM NOT DONE

// TODO
// Compute a number X which verify X + 1 < X using unsigned int
func test__felt(){
    // FILL ME
    let z = x + 1;
    %{ assert ids.z < ids.x, f'assert failed: {ids.z} >= {ids.x}' %}
    return();
}
