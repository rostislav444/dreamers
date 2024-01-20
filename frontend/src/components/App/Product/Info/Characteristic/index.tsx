import {Box, Heading, Table, TableContainer, Tbody, Td, Tr} from '@chakra-ui/react'
import {ProductInterface} from "@/interfaces/Product";
import {InfoHeading} from "@/components/Shared/Typogrphy";

interface ProductCharacteristicsProps {
    product: ProductInterface,
    materialsSelected: any[]
}


const TdStyledLeft = ({children}: { children: any }) => <Td w={52} px={0} pb={3} borderBottom="none">{children}</Td>
const TdStyled = ({children}: { children: any }) => <Td px={0} pb={3} borderBottom="none">{children}</Td>

export const ProductCharacteristics = ({product, materialsSelected}: ProductCharacteristicsProps) => {
    return <Box>
        <InfoHeading>Характеристики</InfoHeading>
        <Box mt='4' >
            <TableContainer>
                <Table size='sm'>
                    <Tbody>
                        <Tr>
                            <TdStyledLeft>Ширина</TdStyledLeft>
                            <TdStyled>{product.width} см.</TdStyled>
                        </Tr>
                        <Tr>
                            <TdStyledLeft>Висота</TdStyledLeft>
                            <TdStyled>{product.height} см.</TdStyled>
                        </Tr>
                        <Tr>
                            <TdStyledLeft>Глибина</TdStyledLeft>
                            <TdStyled>{product.depth} см.</TdStyled>
                        </Tr>
                        {...materialsSelected.map((mat, key) => <Tr key={key}>
                            <TdStyledLeft>{mat.name}</TdStyledLeft>
                            {mat.material.color && <TdStyled>{mat.material.color.name}</TdStyled>}

                        </Tr>)}
                    </Tbody>
                </Table>
            </TableContainer>
        </Box>

    </Box>
}

