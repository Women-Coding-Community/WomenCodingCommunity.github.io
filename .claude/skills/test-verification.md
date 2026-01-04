# Certificate Verification Testing Skill

Test the certificate verification system end-to-end:
- QR code functionality
- Verification page interactions
- Registry lookup accuracy
- Error handling
- User experience flow

## Process

1. Check certificate registry JSON structure
2. Validate QR code generation
3. Test verification page JavaScript:
   - URL parameter parsing
   - Certificate lookup
   - Valid certificate display
   - Invalid certificate handling
   - Error states
4. Check accessibility of verification UI
5. Test with sample certificate IDs
6. Verify mobile responsiveness
7. Check cross-browser compatibility

## Test Cases

- ✓ Valid certificate ID lookup
- ✓ Invalid certificate ID handling
- ✓ Empty input validation
- ✓ URL parameter auto-verification
- ✓ QR code scanning flow
- ✓ Registry file loading errors
- ✓ Network error handling
- ✓ Mobile device usability

## Example Usage

User: "Test the certificate verification system"
Assistant: *Uses this skill to comprehensively test the verification flow*