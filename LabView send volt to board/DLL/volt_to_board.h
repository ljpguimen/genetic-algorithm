#include "extcode.h"
#pragma pack(push)
#pragma pack(1)

#ifdef __cplusplus
extern "C" {
#endif

/*!
 * This VI writes the <b>values to write</b> to the <b>addresses</b> for the 
 * specified <b>board</b>.
 */
int32_t __cdecl Volt_to_board_0(void);
/*!
 * This VI writes the <b>values to write</b> to the <b>addresses</b> for the 
 * specified <b>board</b>.
 */
int32_t __cdecl Volt_to_board_1(void);

MgErr __cdecl LVDLLStatus(char *errStr, int errStrLen, void *module);

#ifdef __cplusplus
} // extern "C"
#endif

#pragma pack(pop)

