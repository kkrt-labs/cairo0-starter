%lang starknet

// Short strings really are felts in disguise, and support the same basic operations

// I AM NOT DONE

// TODO: Find the key to decode the string that passes the test

func decode_cipher1() -> felt {
    // let ciphertext = 'Another One Bites The Dust';
    // let key = 0;
    // let plaintext = ciphertext + key;

    let ciphertext = 'Another One Bites The Dust';
    // let key = 34642338947246174141841020580919298249066932857229157879292816894
    let key = 'Twinkle Twinkle Little Star' - 'Another One Bites The Dust';
    let plaintext = ciphertext + key;

    return plaintext;
}

// TODO: Find the correct ciphertext that passes the test

func decode_cipher2() -> felt {
    // let ciphertext = 0;
    // let plaintext = 1337 * ciphertext + 0xc0de;
    let ciphertext = ('Magic Starknet Money' - 0xc0de) / 1337;
    let plaintext = 1337 * ciphertext + 0xc0de;
    return plaintext;
}

// Do not change the test
func test_decode_string{syscall_ptr: felt*}() {
    // The correct key should produce the corresponding plaintext
    let decoded_string = decode_cipher1();
    assert decoded_string = 'Twinkle Twinkle Little Star';

    // The correct ciphertext should produce corresponding plaintext
    let decoded_string = decode_cipher2();
    assert decoded_string = 'Magic Starknet Money';

    return ();
}
