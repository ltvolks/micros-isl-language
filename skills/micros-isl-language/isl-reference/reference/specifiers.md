# ISL reference: specifiers

Source: RES 3700 SIM Online Help (CHM). Each entry starts with `## ` and the page name; grep `^## ` for an index.


---

## (-) Specifier

<!-- src: Input_Specifiers_Minus_Specifier.htm -->

**(-) Specifier**

### Usage
Data being typed in by the operator should not be echoed back to the display.

**(-) Specifier Example**
```isl
Input auth_code{-}, "Enter authorization code"
```

---

## (Mn, field, start, count | *) Specifier

<!-- src: Input_Specifiers_Magnetic_Track_with_offset_and_count_Specifier.htm -->

(Mn, field, start, count | *) Specifier

### Usage
Mn: the track number (M2); this can be followed by a star (*) to specify all fields on the track, or use the following fields to read specific information:
field: the field position within the specified track; this is a positive integer
start: starting offset (character) within the field; for example, if you want to take the last four characters of the "Blaine Richard" string, you would start the offset at 11
count: number of characters to be read from the start (first character) to the end of the field (place an asterisk * to include all characters)

**(Mn, field, start, count | *) Specifier Example:**
```isl
Input auth_code{ M2,1,3,10 }, \
"Enter authorization code"
```

---

## (Mn,*) Specifier

<!-- src: Input_Specifiers_Magnetic_Track_Specifier.htm -->

**(Mn,*) Specifier**

### Usage
Specify the track number (n = 2) and what data to read from the magnetic card. For use with the Input, InputKey, DisplayInput, and DisplayMSInput commands only. The M character is case-insensitive.

**(Mn,*) Specifier Example**
```isl
Input auth_code{ M2,* }, "Enter authorization code"
```

---

## Binary

<!-- src: Output_Specifiers_Binary_(B).htm -->

Binary (B)

**Usage:**
Binary; displays numerics in binary format

---

## Decimal

<!-- src: Output_Specifiers_Decimal_(D).htm -->

Decimal (D)

**Usage:**
Decimal (default); display numerics in decimal format.

---

## Equality (=)

<!-- src: Output_Specifiers_Equality_(=).htm -->

Equality (=)

**Usage:**

Center justification; the size specifier may be used to specify the size of the field.

---

## format_string

<!-- src: Output_Specifiers_format_string.htm -->

format_string

**Usage:**

Similar the the BASIC language PRINT USING command. All characters will be displayed except for the # character, which will be replaced by characters from the variable or expression preceding the format specifier.

---

## Hexadecimal (X)

<!-- src: Output_Specifiers_Hexadecimal_(X).htm -->

Hexadecimal (X)

**Usage:**
Hexadecimal; displays numerics in hexadecimal format

---

## Input Specifiers

<!-- src: Input_Specifiers.htm -->

Input Specifiers

---

## Leading/Trailing Spaces(*)

<!-- src: Output_Specifiers_Leading_Trailing_Spaces.htm -->

Leading/Trailing Spaces(*)

**Usage:**

Trim leading and trailing spaces; the size specifier may be used to specify the size of the field.

---

## Left Justification (<)

<!-- src: Output_Specifiers_Left_Justification.htm -->

Left Justification (<)

**Usage:**

Left justification; the size specifier may be used to specify the size of the field.

---

## Octal (O)

<!-- src: Output_Specifiers_Octal_(O).htm -->

Octal (O)

**Usage:**
Octal; displays numerics in octal format

---

## Output Specifiers

<!-- src: Output_Specifiers.htm -->

Output Specifiers

---

## Plus

<!-- src: Output_Specifiers_Plus_(+).htm -->

Plus (+)

**Usage:**

Place sign at start of field

---

## Quotes (")

<!-- src: Output_Specifiers_Quotes.htm -->

Quotes (")

**Usage:**

Place double quote around the data to be displayed.

---

## Right Justification

<!-- src: Output_Specifiers_Right_Justification.htm -->

Right Justification (>)

**Usage:**

Right justification; the size specifier may be used to specify the size of the field.

---

## Size

<!-- src: Output_Specifiers_Size.htm -->

Size

**Usage:**

Where size is the number of the characters in the required field. The size must be a positive integer or an expression that is a positive integer.

---

## Space (^)

<!-- src: Output_Specifiers_Space_(^).htm -->

Space (^)

### Usage
:

Place a space on each side of the data to be displayed.

---

## Zero (0)

<!-- src: Output_Specifiers_Zero_(0).htm -->

Zero (0)

### Usage
Pad with zeroes (as opposed to spaces)
