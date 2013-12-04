<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">{#without html tag xsl work incorrect#}
        <html>
            <p id="place">
                <xsl:value-of select="document/header/place"/>
            </p>
            <h1>
                <xsl:value-of select="document/header/name"/>
            </h1>
            <p id="revisions">
                <xsl:value-of select="document/header/revisions"/>
            </p>

            <p id="description">
                <xsl:value-of select="document/header/description"/>
            </p>

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
                                <xsl:for-each select="comment">
                                    <div class="comment">
                                        <h4>
                                            <xsl:value-of select="."/>
                                        </h4>
                                    </div>
                                </xsl:for-each>
                                <xsl:for-each select="./article">
                                    <h3>
                                        <xsl:value-of select="@name"/>
                                    </h3>
                                    <xsl:for-each select="comment">
                                        <div class="comment">
                                            <h4>
                                                <xsl:value-of select="."/>
                                            </h4>
                                        </div>
                                    </xsl:for-each>
                                    <div id="{@id}">
                                        <a role="button" class="btn" id="getWindow" data-toggle="modal" name="btn_{@id}">Ссылка</a>
                                        <br></br>
                                        <xsl:choose>
                                            <xsl:when test="./item">
                                                <xsl:for-each select="./item">
                                                    <div class="article_id">
                                                        <xsl:apply-templates select="@number"/>.
                                                    </div>
                                                    <article id="{@id}">
                                                        <xsl:value-of select='.'/>
                                                    </article>
                                                    <br/>
                                                </xsl:for-each>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:apply-templates select="."/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                        <xsl:for-each select="./references">
                                            <div class="references">
                                                <b> Ссылки на другие законы </b>
                                                <ul>
                                                    <xsl:for-each select="./reference">
                                                        <li>
                                                            <a href="/{@doc_id}/#{@element}">Документ № <xsl:value-of select="@doc_id"/> Статья № <xsl:value-of select="substring-after(string(@element), '_')"/></a>
                                                        </li>
                                                    </xsl:for-each>
                                                </ul>
                                            </div>
                                        </xsl:for-each>
                                        <xsl:for-each select="./links">
                                            <div class="links">
                                                <b> Документы которые ссылаются на данный закон </b>
                                                <ul>
                                                    <xsl:for-each select="./link">
                                                        <li>
                                                            <a href="/{@doc_id}/#{@element}">Документ № <xsl:value-of select="@doc_id"/> Статья № <xsl:value-of select="substring-after(string(@element), '_')"/></a>
                                                        </li>
                                                    </xsl:for-each>
                                                </ul>
                                            </div>
                                        </xsl:for-each>
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
                                <a role="button" class="btn" id="getWindow" data-toggle="modal" name="btn_{@id}">Ссылка</a>
                                <br></br>
                                <xsl:choose>
                                    <xsl:when test="./item">
                                        <xsl:for-each select="./item">
                                            <div class="article_id"><xsl:apply-templates select="@number"/>.
                                            </div>
                                            <article id="{@id}">
                                                <xsl:apply-templates select="."/>
                                            </article>
                                            <br/>
                                        </xsl:for-each>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:apply-templates select="."/>
                                    </xsl:otherwise>
                                </xsl:choose>
                                <xsl:for-each select="./references">
                                    <div class="references">
                                        <b> Ссылки на другие законы </b>
                                        <ul>
                                            <xsl:for-each select="./reference">
                                                <li>
                                                    <a href="/{@doc_id}/#{@element}">Документ № <xsl:value-of select="@doc_id"/> Статья № <xsl:value-of select="substring-after(string(@element), '_')"/></a>
                                                </li>
                                            </xsl:for-each>
                                        </ul>
                                    </div>
                                </xsl:for-each>
                                <xsl:for-each select="./links">
                                    <div class="links">
                                        <b> Документы которые ссылаются на данный закон </b>
                                        <ul>
                                            <xsl:for-each select="./link">
                                                <li>
                                                    <a href="/{@doc_id}/#{@element}">Документ № <xsl:value-of select="@doc_id"/> Статья № <xsl:value-of select="substring-after(string(@element), '_')"/></a>
                                                </li>
                                            </xsl:for-each>
                                        </ul>
                                    </div>
                                </xsl:for-each>
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
