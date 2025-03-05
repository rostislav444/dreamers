import {Box, Table, TableContainer, Tbody, Td, Tr, Text} from '@chakra-ui/react'
import {ProductInterface} from "@/interfaces/Product";
import {InfoHeading} from "@/components/Shared/Typogrphy";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";

interface ProductCharacteristicsProps {
    product: ProductInterface,
    selectedMaterials: SelectedMaterialsInterface
}


const TdStyledLeft = ({children}: { children: any }) => <Td w={24} px={0} pb={3} borderBottom="none">{children}</Td>
const TdStyled = ({children}: { children: any }) => <Td px={0} pb={3} borderBottom="none">{children}</Td>

export const ProductCharacteristics = ({product, selectedMaterials}: ProductCharacteristicsProps) => {
    const selectedParts = product.material_parts.map((part, i) => {
        return {
            name: part.name,
            material: selectedMaterials[part.blender_name].material_name
        }
    })

    return <Box>
        <InfoHeading>Характеристики</InfoHeading>
        <Box mt='4'>
            <TableContainer>
                <Table size='sm' >
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
                        {...selectedParts.map((mat, key) =>
                            <Tr key={key}>
                                <Td w={24} px={0} pb={3} borderBottom="none" verticalAlign="top">{mat.name}</Td>
                                {mat.material && <Td px={0} pb={3} borderBottom="none" verticalAlign="top">
                                    <Text whiteSpace='break-spaces' color='green'>{mat.material}</Text>
                                </Td>}
                            </Tr>
                        )}
                    </Tbody>
                </Table>
            </TableContainer>
        </Box>

    </Box>
}

