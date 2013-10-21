<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">{#without html tag xsl work incorrect#}
        <html>
            <xsl:value-of select="document/description/place"/>
            <h1>
                <xsl:value-of select="document/description/name"/>
            </h1>
            <xsl:value-of select="document/description/revisions"/>
            <div id="contents" class="contents">
                <xsl:choose>
                    <xsl:when test="//section">
                        <xsl:for-each select="//section">
                            <div class="content_chapters">
                                <a href="#{@id}">
                                    <xsl:value-of select="@name"/>
                                </a>
                            </div>
                            <xsl:for-each select="./article">
                                <div class="content_articles">
                                    <a href="#{@id}">
                                        <xsl:value-of select="@name"/>
                                    </a>
                                </div>
                            </xsl:for-each>
                        </xsl:for-each>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:for-each select="//article">
                            <div class="content_chapters">
                                <a href="#{@id}">
                                    <xsl:value-of select="@name"/>
                                </a>
                            </div>
                        </xsl:for-each>
                    </xsl:otherwise>
                </xsl:choose>
            </div>
            <div id="content">
                <xsl:choose>
                    <xsl:when test="//section">
                        <xsl:for-each select="//section">
                            <div id="{@id}">
                                <h2>
                                    <xsl:value-of select="@name"/>
                                </h2>
                                <xsl:for-each select="./article">
                                    <h3>
                                        <xsl:value-of select="@name"/>
                                    </h3>
                                    <div id="{@id}">
                                        <a role="button" class="btn" id="getWindow" data-toggle="modal" name="btn_{@id}">
                                            Ссылка
                                        </a>
                                        <br></br>
                                        <xsl:choose>
                                            <xsl:when test="./item">
                                                <xsl:for-each select="./item">
                                                    <div class="article_id"><xsl:apply-templates select="@number"/>.
                                                    </div>
                                                    <article id="{@id}"><xsl:apply-templates select="."/>.
                                                    </article>
                                                    <br/>
                                                </xsl:for-each>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:apply-templates select="."/>
                                            </xsl:otherwise>
                                        </xsl:choose>

                                        <div class="references">
                                            <ul>
                                                <xsl:for-each select="./references/reference">
                                                    <b> Ссылки на другие законы </b>
                                                    <li>
                                                        <a href="/{@linked_doc_id}/#{@linked_element}">Документ № <xsl:value-of select="@linked_doc_id"/> Статья № <xsl:value-of select="substring-after(string(@linked_element), '_')"/></a>
                                                    </li>
                                                </xsl:for-each>
                                            </ul>
                                        </div>
                                        <div class="links">
                                            <ul>
                                                <xsl:for-each select="./links/link">
                                                    <b> Документы которые ссылаются на данный закон </b>
                                                    <li>
                                                        <a href="/{@reference_doc_id}/#{@reference_element}">Документ № <xsl:value-of select="@reference_doc_id"/> Статья № <xsl:value-of select="substring-after(string(@reference_element), '_')"/></a>
                                                    </li>
                                                </xsl:for-each>
                                            </ul>
                                        </div>
                                    </div>
                                </xsl:for-each>
                            </div>
                        </xsl:for-each>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:for-each select="//article">
                            <h3>
                                <xsl:value-of select="@name"/>
                            </h3>
                            <div id="{@id}">
                                <a role="button" class="btn" id="getWindow" data-toggle="modal" name="btn_{@id}">
                                    Ссылка
                                </a>
                                <br></br>
                                <xsl:choose>
                                    <xsl:when test="./item">
                                        <xsl:for-each select="./item">
                                            <div class="article_id"><xsl:apply-templates select="@number"/>.
                                            </div>
                                            <article id="{@id}">
                                                <xsl:apply-templates select="."/>.
                                            </article>
                                            <br/>
                                        </xsl:for-each>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:apply-templates select="."/>
                                    </xsl:otherwise>
                                </xsl:choose>
                                <div class="references">
                                    <ul>
                                        <xsl:for-each select="./references/reference">
                                            <b> Ссылки на другие законы </b>
                                            <li>
                                              <a href="/{@linked_doc_id}/#{@linked_element}">Документ № <xsl:value-of select="@linked_doc_id"/> Статья № <xsl:value-of select="substring-after(string(@linked_element), '_')"/></a>
                                            </li>
                                        </xsl:for-each>
                                    </ul>
                                </div>
                                <div class="links">
                                    <ul>
                                        <xsl:for-each select="./links/link">
                                            <b> Документы которые ссылаются на данный закон </b>
                                            <li>
                                                <a href="/{@reference_doc_id}/#{@reference_element}">Документ № <xsl:value-of select="@reference_doc_id"/> Статья № <xsl:value-of select="substring-after(string(@reference_element), '_')"/></a>
                                            </li>
                                        </xsl:for-each>
                                    </ul>
                                </div>
                            </div>
                        </xsl:for-each>
                    </xsl:otherwise>
                </xsl:choose>
            </div>
        </html>
    </xsl:template>
    <xsl:template match="reference">
        <a href="/{@document_id}/{@object_id}">
            <xsl:value-of select="."/>
        </a>
    </xsl:template>
</xsl:stylesheet>