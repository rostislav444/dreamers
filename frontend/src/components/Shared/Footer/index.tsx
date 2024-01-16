import {Box, Text} from "@chakra-ui/react";
import React from "react";


export const Footer = () => <Box w='100%' h='24' mt={12} p='8' bg='brown.500'>
    <Box m={'0 12px '}>
        <Text fontSize="18px" color='white'>
            <Box fontWeight="700" as={'span'}>Dreamers ✨</Box>
            <Box fontWeight="500" as={'span'}> - меблі що надихають</Box>
        </Text>
    </Box>
</Box>
