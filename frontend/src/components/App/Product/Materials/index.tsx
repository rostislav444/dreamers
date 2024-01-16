import {Box, Text, useMediaQuery} from '@chakra-ui/react'
import {ProductPartsInterface} from "@/interfaces/Materials";


interface ProductMaterialsInterface {
    parts: ProductPartsInterface[]
    materials: { [key: number]: number };
    selectSkuByMaterials: any
}

export const ProductMaterials = ({parts, materials, selectSkuByMaterials}: ProductMaterialsInterface) => {
    const [mobile] = useMediaQuery('(max-width: 960px)');

    return <Box mt={mobile ? 4 : 6}>
        {parts.map(part =>
            <Box key={part.id}>
                <Text size='md'>{part.name}</Text>
                {part.material_groups.map(group =>
                    <Box
                        key={group.id}
                        mt={mobile ? 4 : 6}
                        mb={mobile ? 4 : 6}
                        display='grid'
                        gridTemplateColumns={`repeat(auto-fill, minmax(${mobile ? 58 : 72}px, 1fr))`}
                        gap='0px'
                    >
                        {group.materials.map(material =>
                            <Box key={material.id}>
                                <Box
                                    onClick={() => selectSkuByMaterials({[part.id]: material.id})}
                                    w={'60px'}
                                    m={'-4px'}
                                    p='4px'
                                    borderWidth='2px'
                                    borderColor={materials[part.id] === material.id ? 'brown.500' : 'transparent'}
                                    borderRadius='0'
                                    cursor='pointer'
                                    _hover={{
                                        borderColor: 'orange.500'
                                    }}
                                >
                                    {material.color && <Box w={12} h={12} bg={material.color.hex}/>}
                                </Box>
                            </Box>
                        )}
                    </Box>
                )}
            </Box>)
        }
    </Box>
}