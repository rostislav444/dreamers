import {ProductProps} from "@/interfaces/Product";
import {useState} from "react";
import {ProductGallery} from "@/components/App/Product/Galery";
import {Flex, useMediaQuery} from "@chakra-ui/react";
import {ProductInfo} from "@/components/App/Product/Info";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {setInitialMaterials} from "@/utils/Product/Materials";


export const ProductComponent = ({product, skuId}: ProductProps) => {
    const [mobile] = useMediaQuery('(max-width: 960px)');
    const [selectedMaterials, setSelectedMaterials] = useState<SelectedMaterialsInterface>(setInitialMaterials(product.material_parts))

    // useEffect(() => {
    //     const url = new URL(window.location.href)
    //     const materials = url.searchParams.get('materials')?.split(',')?.map(Number)
    //
    //     if (materials?.length === selectedMaterials.length) {
    //         setSelectedMaterials(materials)
    //     }
    //
    // }, []);

    return <Flex mb='2' flexDir={mobile ? 'column' : 'row'}>
        <ProductGallery mobile={mobile} product={product} selectedMaterials={selectedMaterials}/>
        <ProductInfo mobile={mobile} product={product} selectedMaterials={selectedMaterials}
                     setSelectedMaterials={setSelectedMaterials}/>
    </Flex>
}