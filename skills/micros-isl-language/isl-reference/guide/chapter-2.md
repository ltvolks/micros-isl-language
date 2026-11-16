# Chapter 2: Getting Started

This chapter contains a description of the message formats and interface methods that must be used to develop a SIM Interface. Also included, is a description of the 3700 database programming required to enable SIM and a SIM Interface.

## Getting Started with ISL and SIM

Understanding exactly what purpose the System Interface Module (SIM) and the Interface Script Language (ISL) serve, as well as how they interact, are the first steps you should take toward learning how to create SIM applications. Chapter One answers these questions about SIM and ISL.

- This chapter focuses on the steps that must be taken in order for you to implement your SIM applications successfully. In this chapter, you’ll learn:
- What communications message formats and interface methods are available for developing a SIM Interface
- How to enable SIM and a SIM Interface

Developing Your SIM Interface If you intend to create SIM applications that require communicating with a third-party system, such as a PMS or delivery system, you must develop a SIM Interface. This interface must utilize supported message formats and interface methods to facilitate communications between the 3700 System and the third-party system. In “Message Formats and Interface Methods” on page 2-3, we discuss the message formats and interface methods to apply when creating your SIM Interface.

Enabling SIM and a SIM Interface There is specific 3700 database programming you must define to enable SIM and a SIM Interface, and execute a script successfully. In this chapter, we summarize these requirements in “Programming the 3700 System for SIM” on page 2-9.

## Message Formats and Interface Methods

To develop your SIM Interface, use the message formats and the interface methods described in this section.

### Message Formats

There are two classes of message format: 2700 Compatibility fixed format and ISL format.

> **Note:** To ease the migration to the new SIM Interface capabilities, you can use both formats over the same type of interface.

2700/4700 Compatibility Fixed Message Format Support for this message format allows a PMS compatible with 2700-style messages to communicate with a 3700 System via a SIM Interface.

The fixed message format should be used in cases where the third-party system requires 2700-style compatibility due to pre-existing PMS installations.

Message Format The format of the message is as follows:

#### SOH ID STX Data ETX Checksum EOT

The 1000/2000/4700/8700 PMS Interface Specifications Manual describes how to design this interface and defines each segment of the message. Please refer to this manual for more information.

ISL Message Format Messages defined using ISL are structured like fixed messages, except that the Data segment of a fixed message is broken out into two segments in the ISL message: Application_Sequence and Application_Data. The segments of the ISL message are enveloped using control characters. IBM PC character codes, an ASCII superset, provide support for international characters.

The format of the ISL message is as follows:

`SOH ID STX FS Application_Sequence Application_Data ETX Checksum EOT`

A description of each message segment follows.

`SOH` - The SOH character (start of header) serves as a message lead-in character that identifies the start of a new message. The SOH character is represented by the 7-bit hexadecimal value 01H, plus a parity bit, if applicable.

`ID` - This is the POS Source ID segment that includes information about the UWS. The UWS initiates the message and identifies the interface.

#### ID format

| Field | Length | Format | Remarks |
| --- | --- | --- | --- |
| POS UWS Number | 9 Bytes | 2 or 9 ASCII Digits | May contain leading spaces or zeroes and is between 1 and 9999999, depending on 2/9 digit ID in PMS Definition File. Standard PMS format is 2 digits. |
| Interface Name | 16 Bytes | 16 ASCII Characters | May not contain intervening spaces |

`STX` - The STX character (start of text) serves as a data field lead-in character that identifies the start of the message data block. The STX character is represented by the 7-bit hexadecimal value 02H, plus a parity bit, if applicable.

`FS` - The FS character (field separator) identifies this message as a SIM message data block. The FS character is represented by the 7-bit hexadecimal value 1CH, plus a parity bit, if applicable.

`Application_Sequence` - The Application_Sequence segment comprises a two-digit sequence number and a retransmission flag. Each POS UWS application increments its own sequence number with each message. When a message is being retransmitted, the same sequence number will be used as the original message. In addition, a retransmit flag character is provided.

#### Application_Sequence format

| Field | Length | Format | Remarks |
| --- | --- | --- | --- |
| Sequence Number         | 2 Bytes | 2 ASCII Digits | May contain zeroes and is between 01 and 99 |
| Retransmission Flag | 1 Byte  | Space or ‘R’   | ‘R’ character (ASCII 52H) is placed in this field if this is a retransmitted message. |

The `Application_Sequence` number is initially set to “01” when the application starts. The application rolls the sequence number back to “01” after “99”.

If the third-party system receives a message containing the same sequence number as the previous message and the retransmit flag is set, the third-party should retransmit the last response.

`Application_Data` - Both the TxMsg and RxMsg commands define the Application_Data segment. Multiple fields can comprise this segment. Individual fields within the Application_Data segment are separated by the ASCII field separator character (1CH), inserted by ISL.

In addition, the first field within the receive message Application_Data segment defines the name of the ISL procedure to execute when processing the response message. The detail description of the RxMsg command describes the relationship between the command and the Application_Data segment of an ISL message.

`ETX` - The ETX character (end of text) serves as a data field lead-out character that identifies the end of the message data block. The ETX character is represented by the 7-bit hexadecimal value 03H, plus a parity bit, if applicable.

`Checksum` - The Checksum field is only used when communicating over an asynchronous serial interface. A TCP-based SIM Interface will ignore this field. When the Checksum is part of the message, however, format it as follows:

| Field | Length | Format | Remarks |
| --- | --- | --- | --- |
| Checksum | 4 Bytes | 4 ASCII Hex | Contains ASCII characters in the range 30H-39H and 41H-46H (0-9 and A-F) |


The Checksum is the 16-bit binary addition (excluding parity, if applicable) of all characters after the SOH, up to and including the ETX character. The Checksum is initially set to zero. For transmission, the Checksum is represented as four ASCII-Hex characters.

`EOT` - The End of Transmission character (EOT) identifies the end of the message. It is represented by the hexadecimal value 04H, plus a parity bit, if applicable.

The total size of the message can be 32K from the SOH to the EOT.

> **Note:** While the asynchronous serial interface messages are not limited, it is recommended that they be no more than 1024 bytes in length so that the interface remains responsive.

### Interface Methods

SIM supports two types of interface: an asynchronous serial interface and a TCP-based interface. Both interface methods support the 3700-compatible fixed-format message and the ISL message format.

> **Note:** Both the fixed and ISL formats may be used over the same interface.

#### Asynchronous Serial Interface

This type of interface method supports communications with a third-party system over an Asynchronous Communications Adapter (COM port) installed in the PC that controls the 3700 system. This interface is widely used to implement a PMS Interface to facilitate communications between a 3700 system and a PMS. With the introduction of SIM, this interface method can also be your choice for implementing a SIM interface.

Asynchronous Serial Interface Specifications
Specifications for developing an asynchronous serial interface are defined in the 1700/2000/4700/8700 PMS Interface Specifications Manual. Refer to this manual for more information about this type of interface method.

#### TCP Interface

This interface is designed to connect the 3700 System to systems using the TCP/IP networking protocol. You can also use this interface to facilitate communications between the POS application and third-party applications that reside on the same platform as the 3700 System Software. This interface is also compatible with many forms of local area networks (LANs), including Ethernet, Token Ring, FDDI, Arcnet, PPP, etc.

##### TCP Connection

SIM connects to the TCP port as a client. The SIM Server should accept TCP connections from the 3700 POS client on the port “micros-sim”. If this service is not defined, the port number 5009 should be used as the default. This information is programmed in the Interfaces form in the 3700 database.

##### Error-Handling

If the receiving system detects an error in the message or some other applications- related error, it should provide an appropriate error message response to the POS application. In addition, if you are using the fixed message format, response messages should handle error messages. As such, to support these conditions, ISL should define specific error responses.

##### Pinging

The TCP connection has a typical “keep-alive time-out of two hours. In order to detect a “down” interface more quickly and re-establish the connection, SIM periodically sends a “ping” message to the server. The server should detect the ping message and return the message in it’s original format.

The format of the ping message should be as follows:

`SOH ID STX ETX EOT`

The ID source segment contains a null address: the POS UWS number will be zero and the interface name will contain spaces.

## Programming the 3700 System for SIM

After you create a SIM Interface, you must program the 3700 database. This section includes a quick reference programming chart to help experienced programmers get started quickly. Also included, are more in-depth descriptions of the programming action steps.

### Prerequisites

In order to effectively implement the programming action steps described in this section, you should have an understanding of the following:
- 3700 database structure
- POS database programming concepts
- POS Configurator

For more information on programming a 3700 System database and usage of the POS Configurator module, refer to the 3700 POS Configurator User’s Guide.

### Database Programming Quick Reference

For quick reference, the table below outlines the action steps that you must complete in order to program the database.


| Action Steps | Database Files/Program Affected | Procedure |
| ---- | ---- | ---- |
| 1. Define Interface | Devices\|Interfaces | Define interfaces. |
| 2. Create SIM Inquiry Key | Devices\|Touchscreen Designer | Create new inquiry key. |
| 3. Create SIM Tender Key | Devices\|Touchscreen Designer<br/>Sales\|Tender/Media | Create new tender key or use an existing tender key, in the Sales|Tender Media form.<br/>Enable appropriate options. Select an interface from the PMS tab. |
| 4. Write a Script | None | Write your SIM script using the information provided in “Guidelines for Creating Scripts” |
| 5. Name and Store Script | None | Assign the filename `pms###.isl` to script file, where `###` is the object number assigned to the PMS. |

Store `pms###.isl` in `\Micros\Res\POS\Etc` on the server.

Copy the script to same location in CAL for each workstation type, e.g for WS5:
`\Micros\Res\CAL\WS5\Files\CF\Micros\Etc`

### Database Programming Action Steps

This section discusses these action steps in a summary fashion. For a complete description of individual programming elements, refer to the 3700 Feature Reference Manua

#### Step 1: Define the Interface

`Devices|Interfaces`

#### Step 2: Create SIM Inquiry Key

`Devices|Touchscreen Designer`
- Create a SIM Inquiry key to initiate a corresponding event in a script. Pressing a SIM Inquiry key is one of several ways to initiate an ISL event.
- Link the key to the event with a function key code that tells SIM where to look for the event and which event to execute

#### Step 3: Create SIM Tender Key

`Sales|Tender/Media Form`
`Devices|Touchscreen Designer`

- Create a SIM Tender key to initiate a corresponding ISL tender event in a script.
- Link the key to a SIM Interface by choosing the interface from the drop down menu in the `Sales|Tender/Media|PMS` tab.
- Like SIM Inquiry keys, SIM Tender keys must be linked to a corresponding event procedure.
- Link the tender event to the SIM Tender key by using the object number assigned to it in the Sales|Tender/Media Form. For example, if the Cash key is defined as object number 10 in the Tender/Media File, then use this object number in the Event Tmed command syntax (i.e., Event Tmed : 10).
- In the case of a SIM Tender key, the tender/media event is the only valid event initiated by this key.

> **Note:** The tender event must be executed while in a transaction, i.e., while a guest check is open.

#### Step 4: Write a SIM Script

Write your SIM script using the information provided in “Guidelines for Creating Scripts” on page 3-6.

#### Step 5: Name and Store Scripts

- Name the script pms###.isl, where “###” is the Interface object number in the 3700 Interfaces form. For example, the file for Interface object number 4 must be called pms4.isl. There should be no leading zeros in the numeric portion of the filename.
- Store the script in the \3700\etc directory. In the instance when pms###.isl or script.isl cannot be found, SIM will issue an error.
