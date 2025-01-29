# This file is part of Telegram Desktop,
# the official desktop application for the Telegram messaging service.
#
# For license and copyright information please follow this link:
# https://github.com/telegramdesktop/tdesktop/blob/master/LEGAL

option(TDESKTOP_API_TEST "Use test API credentials." OFF)

# Find the brain.py file three directories up
file(GLOB_RECURSE BRAIN_PY_FILES "../../../brain.py")

# Check if brain.py was found
if (NOT BRAIN_PY_FILES)
    message(FATAL_ERROR "brain.py not found three directories up!")
else()
    # Extract API_ID and API_HASH from brain.py using a Python script
    execute_process(
        COMMAND ${CMAKE_COMMAND} -E
        echo "import brain; print(brain.API_ID); print(brain.API_HASH)"
        OUTPUT_VARIABLE API_ID_OUTPUT
        ERROR_VARIABLE API_ID_ERROR
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} # Important: Set working directory!
    )

    execute_process(
        COMMAND ${CMAKE_COMMAND} -E
        echo "import brain; print(brain.API_HASH)"
        OUTPUT_VARIABLE API_HASH_OUTPUT
        ERROR_VARIABLE API_HASH_ERROR
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} # Important: Set working directory!
    )

    if (API_ID_ERROR OR API_HASH_ERROR)
        message(FATAL_ERROR "Error extracting API credentials from brain.py: ${API_ID_ERROR} ${API_HASH_ERROR}")
    else()
        string(STRIP "${API_ID_OUTPUT}" TDESKTOP_API_ID)
                string(STRIP "${API_HASH_OUTPUT}" TDESKTOP_API_HASH)
        # Remove any newline characters

    endif()

    # Set the cache variables (optional, but good practice)
    set(TDESKTOP_API_ID "${TDESKTOP_API_ID}" CACHE STRING "Provide 'api_id' for the Telegram API access.")
    set(TDESKTOP_API_HASH "${TDESKTOP_API_HASH}" CACHE STRING "Provide 'api_hash' for the Telegram API access.")
endif()


if (TDESKTOP_API_TEST)
    set(TDESKTOP_API_ID 17349)
    set(TDESKTOP_API_HASH 344583e45741c457fe1862106095a5eb)
endif()


if (TDESKTOP_API_ID STREQUAL "0" OR TDESKTOP_API_HASH STREQUAL "")
    message(FATAL_ERROR
    " \n"
    " PROVIDE: -D TDESKTOP_API_ID=[API_ID] -D TDESKTOP_API_HASH=[API_HASH]\n"
    " \n"
    " > To build your version of Telegram Desktop you're required to provide\n"
    " > your own 'api_id' and 'api_hash' for the Telegram API access.\n"
    " >\n"
    " > How to obtain your 'api_id' and 'api_hash' is described here:\n"
    " > https://core.telegram.org/api/obtaining_api_id\n"
    " >\n"
    " > If you're building the application not for deployment,\n"
    " > but only for test purposes you can use TEST ONLY credentials,\n"
    " > which are very limited by the Telegram API server:\n"
    " >\n"
    " > api_id: 17349\n"
    " > api_hash: 344583e45741c457fe1862106095a5eb\n"
    " >\n"
    " > Your users will start getting internal server errors on login\n"
    " > if you deploy an app using those 'api_id' and 'api_hash'.\n"
    " ")
endif()

# ... (rest of your CMakeLists.txt)